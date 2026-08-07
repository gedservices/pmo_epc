"""
Vues du module Documents.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, FileResponse, Http404
from django.urls import reverse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import Document, DocumentRevision
from .forms import DocumentForm
from .filters import DocumentFilter
from .services import get_statistiques_documents
from apps.core_ref.models import StatutCycleVie


# ============================================================
# DASHBOARD
# ============================================================

@login_required
def dashboard(request):
    """Dashboard GED enrichi."""

    # Statistiques globales
    stats = get_statistiques_documents()

    # Documents récents (derniers 10)
    documents_recents = Document.objects.filter(
        est_archive=False  # ⭐ CORRIGÉ
    ).select_related(
        'projet', 'commande', 'phase', 'statut_actuel'
    ).order_by('-date_creation')[:10]

    # Documents en revue (IFR, IFA)
    documents_en_review = Document.objects.filter(
        statut_actuel__code__in=['IFR', 'IFA'],
        est_archive=False  # ⭐ CORRIGÉ
    ).select_related('projet', 'phase', 'statut_actuel')[:10]

    # Documents en retard de revue (plus de 15 jours)
    date_limite = timezone.now() - timedelta(days=15)
    documents_retard = Document.objects.filter(
        statut_actuel__code__in=['IFR', 'IFA'],
        date_emission__lt=date_limite,
        est_archive=False  # ⭐ CORRIGÉ
    ).select_related('projet', 'phase', 'statut_actuel').order_by('date_emission')[:10]

    # Statistiques par phase
    stats_par_phase = Document.objects.filter(
        est_archive=False  # ⭐ CORRIGÉ
    ).values(
        'phase__code', 'phase__nom'
    ).annotate(
        total=Count('id')
    ).order_by('-total')[:10]

    # Statistiques par discipline
    stats_par_discipline = Document.objects.filter(
        est_archive=False  # ⭐ CORRIGÉ
    ).values(
        'discipline__code', 'discipline__nom'
    ).annotate(
        total=Count('id')
    ).order_by('-total')[:10]

    # Statistiques par type de document
    stats_par_type = Document.objects.filter(
        est_archive=False  # ⭐ CORRIGÉ
    ).values(
        'type_doc__code', 'type_doc__libelle'
    ).annotate(
        total=Count('id')
    ).order_by('-total')[:10]

    # Évolution documentaire sur 6 derniers mois (par mois)
    six_mois_avant = timezone.now() - timedelta(days=180)
    docs_par_mois = Document.objects.filter(
        date_creation__gte=six_mois_avant,
        est_archive=False  # ⭐ CORRIGÉ
    ).extra(
        select={'mois': "DATE_TRUNC('month', date_creation)"}
    ).values('mois').annotate(
        nombre=Count('id')
    ).order_by('mois')

    # Préparer les données pour le graphique
    labels_mois = []
    data_mois = []
    for item in docs_par_mois:
        labels_mois.append(item['mois'].strftime('%B %Y'))
        data_mois.append(item['nombre'])

    # Statistiques par statut (utiliser statut_actuel au lieu de statut_global)
    stats_par_statut = Document.objects.filter(
        est_archive=False  # ⭐ CORRIGÉ
    ).values(
        'statut_actuel__code'
    ).annotate(
        total=Count('id')
    ).order_by('-total')

    # Préparer pour graphique en donut
    labels_statut = [item['statut_actuel__code'] or 'Non défini' for item in stats_par_statut]
    data_statut = [item['total'] for item in stats_par_statut]

    context = {
        'page_title': 'Dashboard GED',
        'stats': stats,
        'documents_recents': documents_recents,
        'documents_en_review': documents_en_review,
        'documents_retard': documents_retard,
        'stats_par_phase': stats_par_phase,
        'stats_par_discipline': stats_par_discipline,
        'stats_par_type': stats_par_type,
        'labels_mois': labels_mois,
        'data_mois': data_mois,
        'labels_statut': labels_statut,
        'data_statut': data_statut,
    }

    return render(request, 'documents/dashboard.html', context)


# ============================================================
# LIST
# ============================================================

@login_required
def document_list(request):
    """Liste des documents avec filtres."""

    queryset = Document.objects.filter(
        est_archive=False  # ⭐ CORRIGÉ
    ).select_related(
        'projet', 'commande', 'phase', 'discipline',
        'classe', 'type_doc', 'origine',
        'responsable',
    ).order_by('-date_creation')

    # Filtres
    filterset = DocumentFilter(request.GET, queryset=queryset)
    documents_filtres = filterset.qs

    nb_total = documents_filtres.count()

    # Pagination
    paginator = Paginator(documents_filtres, 25)
    page = paginator.get_page(request.GET.get('page', 1))

    # Filtres actifs pour affichage
    search = request.GET.get('q', '')
    filtre_statut = request.GET.get('statut_actuel', '')
    filtre_classe = request.GET.get('classe', '')
    filtre_projet = request.GET.get('projet', '')
    filtre_phase = request.GET.get('phase', '')
    filtre_discipline = request.GET.get('discipline', '')

    return render(request, 'documents/list.html', {
        'page_title': 'Documents',
        'documents': page,
        'filterset': filterset,
        'nb_total': nb_total,
        'search': search,
        'filtre_statut': filtre_statut,
        'filtre_classe': filtre_classe,
        'filtre_projet': filtre_projet,
        'filtre_phase': filtre_phase,
        'filtre_discipline': filtre_discipline,
    })


# ============================================================
# CYCLE DE VIE
# ============================================================

@login_required
def document_lifecycle(request):
    """
    Vue cycle de vie des documents.
    Affiche l'état d'avancement de chaque document dans son cycle.
    """
    queryset = Document.objects.filter(
        est_archive=False  # ⭐ CORRIGÉ
    ).select_related(
        'projet', 'commande', 'phase', 'discipline',
        'classe', 'type_doc', 'origine',
        'responsable', 'statut_actuel'
    ).order_by('-date_creation')

    # Filtres
    filterset = DocumentFilter(request.GET, queryset=queryset)
    documents_filtres = filterset.qs

    # Récupérer la séquence attendue pour chaque document
    documents_avec_sequence = []
    for doc in documents_filtres:
        # Calculer la séquence de statuts attendue
        sequence_statuts = []
        if doc.phase and doc.classe:
            from .services import get_sequence_statuts

            # Vérifier si le document est un plan (à adapter selon votre logique)
            est_plan = False
            if doc.type_doc:
                # Types considérés comme plans
                types_plans = ['P&ID', 'ISO', 'PFD', 'GA', 'SLD', 'ELD', 'DRW']
                est_plan = doc.type_doc.code in types_plans

            sequence_codes = get_sequence_statuts(
                doc.phase.code,
                doc.classe.numero,
                est_plan
            )
            # Récupérer les objets StatutCycleVie correspondants
            for code in sequence_codes:
                statut = StatutCycleVie.objects.filter(code=code).first()
                if statut:
                    sequence_statuts.append(statut)

        # Déterminer le % d'avancement dans le cycle
        progression_cycle = 0
        index_actuel = 0
        if doc.statut_actuel and sequence_statuts:
            try:
                index_actuel = [s.code for s in sequence_statuts].index(doc.statut_actuel.code)
                progression_cycle = int((index_actuel + 1) / len(sequence_statuts) * 100)
            except ValueError:
                progression_cycle = 0

        documents_avec_sequence.append({
            'document': doc,
            'sequence': sequence_statuts,
            'index_actuel': index_actuel,
            'progression_cycle': progression_cycle,
        })

    # Statistiques
    nb_total = documents_filtres.count()

    # Pagination
    paginator = Paginator(documents_avec_sequence, 25)
    page = paginator.get_page(request.GET.get('page', 1))

    # Filtres actifs
    search = request.GET.get('q', '')
    filtre_projet = request.GET.get('projet', '')
    filtre_commande = request.GET.get('commande', '')
    filtre_phase = request.GET.get('phase', '')
    filtre_classe = request.GET.get('classe', '')

    return render(request, 'documents/lifecycle.html', {
        'page_title': 'Cycle de Vie Documents',
        'documents_page': page,
        'filterset': filterset,
        'nb_total': nb_total,
        'search': search,
        'filtre_projet': filtre_projet,
        'filtre_commande': filtre_commande,
        'filtre_phase': filtre_phase,
        'filtre_classe': filtre_classe,
    })


# ============================================================
# VUE PAR ÉTAT
# ============================================================

@login_required
def document_status_view(request):
    """
    Vue des documents par état.
    Regroupe : finis, non finis, en retard de revue, en cours de revue.
    """
    queryset = Document.objects.filter(
        est_archive=False  # ⭐ CORRIGÉ
    ).select_related(
        'projet', 'commande', 'phase', 'statut_actuel',
        'classe', 'type_doc'
    )

    # Définir les délais de revue par défaut
    DELAI_REVUE_COMPANY = 15  # jours

    # Documents finalisés (statut terminal)
    docs_finalises = queryset.filter(
        statut_actuel__est_terminal=True
    ).order_by('-date_emission')

    # Documents en cours (statut IFR, IFA)
    docs_en_cours = queryset.filter(
        statut_actuel__code__in=['IFR', 'IFA']
    ).order_by('-date_creation')

    # Documents en revue (IFR, IFA récents)
    date_limite = timezone.now() - timedelta(days=DELAI_REVUE_COMPANY)
    docs_en_revue = queryset.filter(
        statut_actuel__code__in=['IFR', 'IFA'],
        date_emission__gte=date_limite
    ).order_by('-date_emission')

    # Documents en retard de revue (plus de X jours en IFR/IFA)
    docs_retard_revue = queryset.filter(
        statut_actuel__code__in=['IFR', 'IFA'],
        date_emission__lt=date_limite
    ).order_by('date_emission')

    # Statistiques
    stats = {
        'total': queryset.count(),
        'finalises': docs_finalises.count(),
        'en_cours': docs_en_cours.count(),
        'en_revue': docs_en_revue.count(),
        'en_retard': docs_retard_revue.count(),
    }

    # Onglet actif
    onglet = request.GET.get('onglet', 'finalises')

    # Pagination selon l'onglet
    if onglet == 'finalises':
        docs = docs_finalises
    elif onglet == 'en_cours':
        docs = docs_en_cours
    elif onglet == 'en_revue':
        docs = docs_en_revue
    elif onglet == 'en_retard':
        docs = docs_retard_revue
    else:
        docs = docs_finalises

    paginator = Paginator(docs, 25)
    page = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'documents/status.html', {
        'page_title': 'État des Documents',
        'documents': page,
        'stats': stats,
        'onglet': onglet,
        'delai_revue': DELAI_REVUE_COMPANY,
    })


# ============================================================
# DETAIL
# ============================================================

@login_required
def document_detail(request, pk):
    """Détail d'un document."""

    document = get_object_or_404(
        Document.objects.select_related(
            'projet', 'commande', 'phase', 'discipline',
            'classe', 'type_doc',
            'responsable', 'origine',
        ),
        pk=pk,
        est_archive=False  # ⭐ CORRIGÉ
    )

    revisions = document.revisions.select_related(
        'statut', 'auteur_revision'
    ).order_by('-ordre')

    return render(request, 'documents/detail.html', {
        'page_title': document.code_documentaire,
        'document': document,
        'revisions': revisions,
    })


# ============================================================
# CREATE
# ============================================================

@login_required
def document_create(request):
    """Création d'un document."""

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                doc = form.save(commit=False)
                doc.revision_actuelle = 'rev00'
                doc.est_archive = False  # ⭐ CORRIGÉ
                doc.save()

                messages.success(
                    request,
                    f"Document {doc.code_documentaire} créé avec succès."
                )
                return redirect('documents:detail', pk=doc.pk)
            except Exception as e:
                messages.error(request, f"Erreur : {e}")
    else:
        form = DocumentForm()

    return render(request, 'documents/form.html', {
        'page_title': 'Nouveau Document',
        'form': form,
        'action': 'create',
        'cancel_url': reverse('documents:list'),
    })