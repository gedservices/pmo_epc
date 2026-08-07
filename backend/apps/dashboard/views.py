from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Avg, Sum, Count
from apps.projects.models import Projet
from apps.tasks.models import Tache
from apps.risks.models import Risque
from apps.core_ref.models import Conteneur


@login_required
def index(request):
    # Redirect racine vers dashboard
    return dashboard(request)


@login_required
def dashboard(request):
    # Conteneur actif
    cid = request.session.get('conteneur_actif_id')
    conteneur = None
    if cid:
        conteneur = Conteneur.objects.filter(id=cid, actif=True).first()
    if not conteneur:
        conteneur = Conteneur.objects.filter(code='RUNNING', actif=True).first()

    # Projets du conteneur
    projets = Projet.objects.filter(
        conteneur=conteneur,
        est_generique=False
    ).select_related('responsable', 'site', 'conteneur')

    # KPI
    nb_projets   = projets.count()
    nb_en_retard = sum(1 for p in projets if p.est_en_retard)

    avg_progression = 0
    if nb_projets:
        avg_progression = round(
            sum(float(p.progression_calculee) for p in projets) / nb_projets, 1)

    budget_total_prevu = sum(float(p.budget_prevu) for p in projets)
    budget_total_reel  = sum(float(p.budget_reel)  for p in projets)
    budget_pct         = (round(budget_total_reel / budget_total_prevu * 100, 1)
                          if budget_total_prevu > 0 else 0)

    # Risques critiques (criticité >= 15)
    risques_critiques = [
        r for r in Risque.objects.filter(
            projet__in=projets, statut__in=['Ouvert', 'En cours'])
        if r.criticite >= 15
    ]

    # Tâches en retard
    taches_en_retard = Tache.objects.filter(
        projet__in=projets, est_en_retard=True
    ).count()

    # Données Courbe en S portefeuille (agregé)
    from apps.projects.models import Projet as P
    historiques = []
    for p in projets:
        for h in p.historique_avancement.order_by('date_snapshot'):
            historiques.append({
                'date':   h.date_snapshot.strftime('%Y-%m-%d'),
                'reel':   float(h.avancement_reel or 0),
                'prevu':  float(h.avancement_prevu or 0),
                'pv':     float(h.planned_value or 0),
                'ev':     float(h.earned_value  or 0),
                'ac':     float(h.actual_cost   or 0),
            })

    # Données EVM par projet
    evm_labels = [p.code for p in projets]
    evm_spi    = [float(p.spi or 0) for p in projets]
    evm_cpi    = [float(p.cpi or 0) for p in projets]

    import json
    return render(request, 'dashboard/index.html', {
        'page_title':          'Dashboard PMO',
        'conteneur':           conteneur,
        'projets':             projets,
        'nb_projets':          nb_projets,
        'nb_en_retard':        nb_en_retard,
        'pct_en_retard':       round(nb_en_retard / nb_projets * 100
                                     if nb_projets else 0, 0),
        'avg_progression':     avg_progression,
        'budget_prevu':        budget_total_prevu,
        'budget_reel':         budget_total_reel,
        'budget_pct':          budget_pct,
        'risques_critiques':   risques_critiques,
        'nb_risques_critiques': len(risques_critiques),
        'taches_en_retard':    taches_en_retard,
        'historiques_json':    json.dumps(historiques),
        'evm_labels_json':     json.dumps(evm_labels),
        'evm_spi_json':        json.dumps(evm_spi),
        'evm_cpi_json':        json.dumps(evm_cpi),
    })
