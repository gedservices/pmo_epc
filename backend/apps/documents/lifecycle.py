

@login_required
def document_lifecycle(request):
    """
    Vue cycle de vie des documents.
    Affiche l'état d'avancement de chaque document dans son cycle.
    """
    queryset = Document.objects.filter(est_supprime=False).select_related(
        'projet', 'commande', 'phase', 'discipline',
        'classe_documentaire', 'type_technique', 'originator',
        'responsable', 'statut_actuel'
    ).order_by('-date_modification')

    # Filtres
    filterset = DocumentFilter(request.GET, queryset=queryset)
    documents_filtres = filterset.qs

    # Récupérer la séquence attendue pour chaque document
    documents_avec_sequence = []
    for doc in documents_filtres:
        # Calculer la séquence de statuts attendue
        sequence_statuts = []
        if doc.phase and doc.classe_documentaire:
            from .services import get_sequence_statuts
            sequence_codes = get_sequence_statuts(
                doc.phase.code,
                doc.classe_documentaire.numero,
                doc.est_plan
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
    filtre_classe = request.GET.get('classe_documentaire', '')

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


@login_required
def document_status_view(request):
    """
    Vue des documents par état.
    Regroupe : finis, non finis, en retard de revue, en cours de revue.
    """
    from django.utils import timezone
    from datetime import timedelta

    queryset = Document.objects.filter(est_supprime=False).select_related(
        'projet', 'commande', 'phase', 'statut_actuel',
        'classe_documentaire', 'type_technique'
    )

    # Définir les délais de revue par défaut
    DELAI_REVUE_COMPANY = 15  # jours
    DELAI_REVUE_CONTRACTOR = 15  # jours

    # Documents finalisés
    docs_finalises = queryset.filter(est_final=True).order_by('-date_finalisation')

    # Documents en cours (non finalisés)
    docs_en_cours = queryset.filter(est_final=False, statut_global__in=['EN_COURS', 'BROUILLON']).order_by(
        '-date_modification')

    # Documents en revue (IFR, IFA)
    docs_en_revue = queryset.filter(
        statut_actuel__code__in=['IFR', 'IFA'],
        est_final=False
    ).order_by('-date_emission')

    # Documents en retard de revue (plus de X jours en IFR/IFA)
    date_limite = timezone.now() - timedelta(days=DELAI_REVUE_COMPANY)
    docs_retard_revue = queryset.filter(
        statut_actuel__code__in=['IFR', 'IFA'],
        date_emission__lt=date_limite,
        est_final=False
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


@login_required
def dashboard(request):
    """Dashboard GED enrichi."""

    from django.db.models import Count, Q
    from django.utils import timezone
    from datetime import timedelta

    # Statistiques globales
    stats = get_statistiques_documents()

    # Documents récents (derniers 10)
    documents_recents = Document.objects.filter(
        est_supprime=False
    ).select_related(
        'projet', 'commande', 'phase', 'statut_actuel'
    ).order_by('-date_modification')[:10]

    # Documents en revue
    documents_en_review = Document.objects.filter(
        statut_global='EN_REVIEW',
        est_supprime=False
    ).select_related('projet', 'phase', 'statut_actuel')[:10]

    # Documents en retard de revue (plus de 15 jours)
    date_limite = timezone.now() - timedelta(days=15)
    documents_retard = Document.objects.filter(
        statut_actuel__code__in=['IFR', 'IFA'],
        date_emission__lt=date_limite,
        est_final=False,
        est_supprime=False
    ).select_related('projet', 'phase', 'statut_actuel').order_by('date_emission')[:10]

    # Statistiques par phase
    stats_par_phase = Document.objects.filter(
        est_supprime=False
    ).values(
        'phase__code', 'phase__nom'
    ).annotate(
        total=Count('id')
    ).order_by('-total')[:10]

    # Statistiques par discipline
    stats_par_discipline = Document.objects.filter(
        est_supprime=False
    ).values(
        'discipline__code', 'discipline__nom'
    ).annotate(
        total=Count('id')
    ).order_by('-total')[:10]

    # Statistiques par type de document
    stats_par_type = Document.objects.filter(
        est_supprime=False
    ).values(
        'type_technique__code', 'type_technique__libelle'
    ).annotate(
        total=Count('id')
    ).order_by('-total')[:10]

    # Évolution documentaire sur 6 derniers mois (par mois)
    six_mois_avant = timezone.now() - timedelta(days=180)
    docs_par_mois = Document.objects.filter(
        date_creation__gte=six_mois_avant,
        est_supprime=False
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

    # Statistiques par statut
    stats_par_statut = Document.objects.filter(
        est_supprime=False
    ).values(
        'statut_global'
    ).annotate(
        total=Count('id')
    ).order_by('-total')

    # Préparer pour graphique en donut
    labels_statut = [item['statut_global'] for item in stats_par_statut]
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