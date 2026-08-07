from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator
from .models import Projet, MigrationConteneurLog
from .forms import ProjetForm
from apps.core_ref.models import Conteneur


def get_conteneur_actif(request):
    cid = request.session.get('conteneur_actif_id')
    if cid:
        return Conteneur.objects.filter(id=cid, actif=True).first()
    return Conteneur.objects.filter(code='RUNNING', actif=True).first()


@login_required
def projet_list(request):
    conteneur = get_conteneur_actif(request)
    qs = Projet.objects.filter(est_generique=False)

    if conteneur:
        qs = qs.filter(conteneur=conteneur)

    # Filtres
    search   = request.GET.get('q', '').strip()
    statut   = request.GET.get('statut', '')
    priorite = request.GET.get('priorite', '')
    site_id  = request.GET.get('site', '')
    sort     = request.GET.get('sort', '-date_modification')

    if search:
        qs = qs.filter(
            Q(code__icontains=search) |
            Q(nom__icontains=search) |
            Q(description__icontains=search)
        )
    if statut:
        qs = qs.filter(statut=statut)
    if priorite:
        qs = qs.filter(priorite=priorite)
    if site_id:
        qs = qs.filter(site_id=site_id)

    # Tri
    valid_sorts = ['code', '-code', 'nom', '-nom',
                   'progression_calculee', '-progression_calculee',
                   'date_fin_prevue', '-date_fin_prevue',
                   '-date_modification']
    if sort in valid_sorts:
        qs = qs.order_by(sort)

    # Pagination
    paginator = Paginator(qs, request.GET.get('per_page', 25))
    page      = paginator.get_page(request.GET.get('page', 1))

    # KPI barre
    all_projets = qs
    nb_retard   = sum(1 for p in all_projets if p.est_en_retard)

    return render(request, 'projects/list.html', {
        'page_title':   'Projets',
        'projets':      page,
        'paginator':    paginator,
        'conteneur':    conteneur,
        'nb_total':     paginator.count,
        'nb_retard':    nb_retard,
        'search':       search,
        'filtre_statut':   statut,
        'filtre_priorite': priorite,
        'filtre_site':     site_id,
        'sort':            sort,
        'statut_choices':  Projet.STATUT_CHOICES,
        'priorite_choices': Projet.PRIORITE_CHOICES,
    })


@login_required
def projet_detail(request, pk):
    projet  = get_object_or_404(Projet, pk=pk)
    onglet  = request.GET.get('onglet', 'general')

    # Recalcul progression à la volée
    projet.recalculer_progression()

    ctx = {
        'page_title': f"{projet.code} — {projet.nom}",
        'projet':     projet,
        'onglet':     onglet,
        'commandes':  projet.commandes.order_by('code_commande'),
        'risques':    projet.risques.order_by('-criticite')[:5],
        'historique': projet.historique_avancement.order_by('date_snapshot'),
    }
    return render(request, 'projects/detail.html', ctx)


@login_required
def projet_create(request):
    if request.method == 'POST':
        form = ProjetForm(request.POST)
        if form.is_valid():
            projet = form.save(commit=False)
            projet.cree_par = request.user
            projet.save()
            form.save_m2m()
            messages.success(request,
                f"Projet {projet.code} créé avec succès.")
            return redirect('projects:detail', pk=projet.pk)
    else:
        form = ProjetForm()

    return render(request, 'projects/form.html', {
        'page_title': 'Nouveau Projet',
        'form':       form,
        'action':     'create',
    })


@login_required
def projet_edit(request, pk):
    projet = get_object_or_404(Projet, pk=pk)
    if projet.est_lecture_seule and not request.user.is_admin:
        messages.error(request, "Ce projet est en lecture seule.")
        return redirect('projects:detail', pk=pk)

    if request.method == 'POST':
        form = ProjetForm(request.POST, instance=projet)
        if form.is_valid():
            projet = form.save(commit=False)
            projet.modifie_par = request.user
            projet.save()
            form.save_m2m()
            messages.success(request, "Projet mis à jour.")
            return redirect('projects:detail', pk=pk)
    else:
        form = ProjetForm(instance=projet)

    return render(request, 'projects/form.html', {
        'page_title': f'Modifier — {projet.code}',
        'form':       form,
        'projet':     projet,
        'action':     'edit',
    })


@login_required
def projet_migrate(request, pk):
    projet = get_object_or_404(Projet, pk=pk)

    if request.method == 'POST':
        conteneur_cible_id = request.POST.get('conteneur_cible')
        commentaire        = request.POST.get('commentaire', '')

        conteneur_cible = get_object_or_404(Conteneur, pk=conteneur_cible_id)

        # Vérification : toutes commandes terminées
        commandes_non_terminees = projet.commandes.exclude(
            statut__in=['Terminée', 'Annulée'])
        if commandes_non_terminees.exists():
            messages.error(request,
                f"{commandes_non_terminees.count()} commande(s) "
                f"non terminée(s). Migration impossible.")
            return redirect('projects:detail', pk=pk)

        # Log migration
        MigrationConteneurLog.objects.create(
            projet=projet,
            conteneur_source=projet.conteneur,
            conteneur_cible=conteneur_cible,
            migre_par=request.user,
            commentaire=commentaire,
        )

        # Migration
        projet.conteneur      = conteneur_cible
        projet.statut         = 'Finalisé'
        projet.est_lecture_seule = True
        projet.save()

        messages.success(request,
            f"Projet {projet.code} migré vers '{conteneur_cible.libelle}'.")
        return redirect('projects:list')

    conteneurs_cibles = Conteneur.objects.filter(
        actif=True).exclude(id=projet.conteneur_id)

    return render(request, 'projects/migrate.html', {
        'page_title':       f'Migrer — {projet.code}',
        'projet':           projet,
        'conteneurs_cibles': conteneurs_cibles,
    })
