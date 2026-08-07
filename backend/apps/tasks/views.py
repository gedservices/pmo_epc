from django.shortcuts import render

# Create your views here.

import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Tache
from .forms import TacheForm
from apps.projects.models import Projet
from apps.contracts.models import Commande
from django.urls import reverse






@login_required
def tache_list(request):
    qs = Tache.objects.select_related(
        'projet', 'commande', 'responsable', 'phase', 'discipline')

    # Filtres
    search      = request.GET.get('q', '').strip()
    statut      = request.GET.get('statut', '')
    projet_id   = request.GET.get('projet', '')
    commande_id = request.GET.get('commande', '')
    discipline  = request.GET.get('discipline', '')
    en_retard   = request.GET.get('en_retard', '')
    sort        = request.GET.get('sort', 'date_fin_prevue')

    if search:
        qs = qs.filter(Q(nom__icontains=search) | Q(description__icontains=search))
    if statut:
        qs = qs.filter(statut=statut)
    if projet_id:
        qs = qs.filter(projet_id=projet_id)
    if commande_id:
        qs = qs.filter(commande_id=commande_id)
    if discipline:
        qs = qs.filter(discipline__code=discipline)
    if en_retard == '1':
        qs = qs.filter(est_en_retard=True)

    valid_sorts = ['nom', '-nom', 'date_fin_prevue', '-date_fin_prevue',
                   'avancement', '-avancement', 'poids', '-poids']
    if sort in valid_sorts:
        qs = qs.order_by(sort)

    paginator = Paginator(qs, request.GET.get('per_page', 25))
    page      = paginator.get_page(request.GET.get('page', 1))

    # ⭐ AJOUT : Querysets pour les filtres dropdown
    from apps.contracts.models import Commande
    from apps.core_ref.models import Discipline

    return render(request, 'tasks/list.html', {
        'page_title':  'Tâches',
        'taches':      page,
        'paginator':   paginator,
        'projets':     Projet.objects.filter(est_generique=False),
        'commandes':   Commande.objects.all(),  # ⭐
        'disciplines': Discipline.objects.all(),  # ⭐
        'search':      search,
        'filtre_statut':    statut,
        'filtre_projet':    projet_id,
        'filtre_commande':  commande_id,
        'filtre_discipline': discipline,
        'filtre_en_retard': en_retard,
        'statut_choices': Tache.STATUT_CHOICES,
        'sort': sort,  # ⭐ Pour les indicateurs de tri
    })






# @login_required
# def tache_list(request):
#     qs = Tache.objects.select_related(
#         'projet', 'commande', 'responsable', 'phase', 'discipline')
#
#     # Filtres
#     search      = request.GET.get('q', '').strip()
#     statut      = request.GET.get('statut', '')
#     projet_id   = request.GET.get('projet', '')
#     commande_id = request.GET.get('commande', '')
#     discipline  = request.GET.get('discipline', '')
#     en_retard   = request.GET.get('en_retard', '')
#     sort        = request.GET.get('sort', 'date_fin_prevue')
#
#     if search:
#         qs = qs.filter(Q(nom__icontains=search) |
#                        Q(description__icontains=search))
#     if statut:
#         qs = qs.filter(statut=statut)
#     if projet_id:
#         qs = qs.filter(projet_id=projet_id)
#     if commande_id:
#         qs = qs.filter(commande_id=commande_id)
#     if discipline:
#         qs = qs.filter(discipline__code=discipline)
#     if en_retard == '1':
#         qs = qs.filter(est_en_retard=True)
#
#     valid_sorts = ['nom', '-nom', 'date_fin_prevue',
#                    '-date_fin_prevue', 'avancement', '-avancement',
#                    'poids', '-poids']
#     if sort in valid_sorts:
#         qs = qs.order_by(sort)
#
#     paginator = Paginator(qs, request.GET.get('per_page', 25))
#     page      = paginator.get_page(request.GET.get('page', 1))
#
#     return render(request, 'tasks/list.html', {
#         'page_title':  'Tâches',
#         'taches':      page,
#         'paginator':   paginator,
#         'projets':     Projet.objects.filter(est_generique=False),
#         'search':      search,
#         'filtre_statut':    statut,
#         'filtre_projet':    projet_id,
#         'filtre_commande':  commande_id,
#         'filtre_discipline': discipline,
#         'filtre_en_retard': en_retard,
#         'statut_choices': Tache.STATUT_CHOICES,
#     })


@login_required
def tache_detail(request, pk):
    tache = get_object_or_404(Tache, pk=pk)
    return render(request, 'tasks/detail.html', {
        'page_title': tache.nom,
        'tache':      tache,
        'historique': tache.historique.all()[:20],
    })


@login_required
def tache_create(request):
    if request.method == 'POST':
        form = TacheForm(request.POST)
        if form.is_valid():
            tache = form.save(commit=False)
            tache.cree_par = request.user
            tache.save()
            messages.success(request, "Tâche créée.")
            return redirect('tasks:detail', pk=tache.pk)
    else:
        form = TacheForm()

    # Mojo comments
    # return render(request, 'tasks/form.html', {
    #     'page_title': 'Nouvelle Tâche',
    #     'form': form, 'action': 'create',
    # })
    return render(request, "tasks/form.html", {
        "page_title": "Nouvelle tâche",
        "form": form,
        "action": "create",
        "cancel_url": reverse("tasks:list"),
    })


@login_required
def tache_edit(request, pk):
    tache = get_object_or_404(Tache, pk=pk)
    if request.method == 'POST':
        form = TacheForm(request.POST, instance=tache)
        if form.is_valid():
            tache = form.save(commit=False)
            tache.modifie_par = request.user
            tache.save()
            tache.projet.recalculer_progression()
            messages.success(request, "Tâche mise à jour.")
            return redirect('tasks:detail', pk=pk)
    else:
        form = TacheForm(instance=tache)

    # MoJo comment
    # return render(request, 'tasks/form.html', {
    #     'page_title': f'Modifier — {tache.nom}',
    #     'form': form, 'tache': tache, 'action': 'edit',
    # })
    return render(request, "tasks/form.html", {
        "page_title": f"Modifier — {tache.nom}",
        "form": form,
        "tache": tache,
        "action": "edit",
        "cancel_url": reverse("tasks:detail", args=[tache.pk]),
    })


@login_required
def tache_delete(request, pk):
    tache = get_object_or_404(Tache, pk=pk)
    if request.method == 'POST':
        projet = tache.projet
        tache.delete()
        projet.recalculer_progression()
        messages.success(request, "Tâche supprimée.")
        return redirect('tasks:list')
    return render(request, 'tasks/confirm_delete.html', {
        'page_title': 'Supprimer Tâche',
        'tache': tache,
    })


@login_required
def gantt(request):
    projet_id = request.GET.get('projet', '')
    projets   = Projet.objects.filter(est_generique=False)
    projet    = None
    if projet_id:
        projet = get_object_or_404(Projet, pk=projet_id)

    return render(request, 'tasks/gantt.html', {
        'page_title': 'Planning Gantt',
        'projets':    projets,
        'projet':     projet,
        'projet_id':  projet_id,
    })


@login_required
def gantt_data(request):
    """API JSON pour le Gantt."""
    projet_id = request.GET.get('projet', '')
    qs = Tache.objects.select_related('commande', 'phase', 'discipline')
    if projet_id:
        qs = qs.filter(projet_id=projet_id)

    data = []
    commandes_vues = set()

    for t in qs:
        # Groupe commande
        if t.commande and t.commande_id not in commandes_vues:
            commandes_vues.add(t.commande_id)
            data.append({
                'id':       f'cmd-{t.commande_id}',
                'text':     f"{t.commande.code_commande} — {t.commande.nom[:40]}",
                'type':     'project',
                'open':     True,
                'readonly': True,
            })

        item = {
            'id':       t.id,
            'text':     t.nom,
            'start_date': t.date_debut_prevue.strftime('%d-%m-%Y')
                          if t.date_debut_prevue else None,
            'end_date':   t.date_fin_prevue.strftime('%d-%m-%Y')
                          if t.date_fin_prevue else None,
            'progress':   float(t.avancement) / 100,
            'parent':     f'cmd-{t.commande_id}' if t.commande else 0,
            'statut':     t.statut,
            'en_retard':  t.est_en_retard,
            'responsable': str(t.responsable) if t.responsable else '',
            'color': ('#E53935' if t.est_en_retard else
                      '#F59E0B' if t.statut == 'En cours' else
                      '#16A34A' if t.statut == 'Terminée' else '#64748B'),
        }
        data.append(item)

    return JsonResponse({'data': data})
