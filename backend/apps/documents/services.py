"""
Services métier du module Documents.
Version simplifiée pour démarrer.
"""

from django.db import transaction
from .models import Document

# ============================================================
# SÉQUENCES DE CYCLE DE VIE
# ============================================================

CYCLE_VIE = {
    # PHASE BE - Basic Engineering
    ('BE', 1): ['IFR', 'IFA', 'AFD'],
    ('BE', 2): ['IFR', 'AFD'],
    ('BE', 3): ['IFI'],

    # PHASE EPC / Construction
    ('EPC', 1): ['IFR', 'IFA', 'AFC', 'MKP', 'ASB'],
    ('EPC', 2): ['IFR', 'AFC', 'MKP', 'ASB'],
    ('EPC', 3): ['IFI'],

    # PHASE DE - Detailed Engineering / Procurement
    ('DE', 1): ['IFR', 'IFA', 'AFC'],
    ('DE', 2): ['IFR', 'AFC'],
    ('DE', 3): ['IFI'],
}


def get_sequence_statuts(phase_code, classe_num, est_plan=False):
    """
    Retourne la séquence de statuts pour une phase donnée et une classe donnée.
    """
    key = (phase_code.upper(), classe_num)
    sequence = CYCLE_VIE.get(key, [])

    if not est_plan:
        # Retirer les statuts spécifiques aux plans
        sequence = [s for s in sequence if s not in ('MKP', 'ASB')]

    return sequence


def get_statistiques_documents(projet=None, commande=None):
    """
    Retourne un dict de statistiques documentaires.
    """
    qs = Document.objects.filter(est_archive=False)

    if projet:
        qs = qs.filter(projet=projet)
    if commande:
        qs = qs.filter(commande=commande)

    return {
        'total': qs.count(),
        'en_review': qs.filter(statut_actuel__code__in=['IFR', 'IFA']).count(),
        'finalises': qs.filter(statut_actuel__est_terminal=True).count(),
        'brouillons': qs.filter(statut_actuel__isnull=True).count(),
        'archives': Document.objects.filter(est_archive=True).count(),
        'par_classe': {
            'classe_1': qs.filter(classe__numero=1).count(),
            'classe_2': qs.filter(classe__numero=2).count(),
            'classe_3': qs.filter(classe__numero=3).count(),
        },
    }