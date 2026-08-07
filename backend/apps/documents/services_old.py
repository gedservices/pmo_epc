from django.db.models import Q
from apps.core_ref.models import SequenceStatut, Phase, StatutCycleVie


class DocumentWorkflowService:
    """
    Gestion du cycle de vie documentaire selon la spec PMO EPC.
    Respecte les classes (1,2,3), phases (BE, EPC, DE, Procurement) et codes retour.
    """

    CODES_RETROU_ACCEPTANTS = ['Accepté sans commentaire', 'Accepté avec commentaire']

    @staticmethod
    def get_sequence_for_context(phase_id, classe_num):
        """Récupère la séquence de statuts autorisée pour une phase et une classe."""
        return SequenceStatut.objects.filter(
            phase_id=phase_id,
            classe_num=classe_num
        ).order_by('ordre')

    @staticmethod
    def get_next_valid_status(current_status_code, sequence):
        """Retourne le statut suivant dans la séquence."""
        try:
            current_idx = sequence.index([s for s in sequence if s.statut.code == current_status_code][0])
            return sequence[current_idx + 1].statut if current_idx < len(sequence) - 1 else sequence[-1].statut
        except (ValueError, IndexError):
            return sequence[0].statut if sequence else None

    @staticmethod
    def validate_progression(current_status, code_retour):
        """
        RG: Un document monte en statut si code_retour est acceptant.
        Si 'Rejeté', la révision monte mais le statut reste.
        """
        if not code_retour:
            return False, "Code retour requis pour progression."

        if code_retour in DocumentWorkflowService.CODES_RETROU_ACCEPTANTS:
            return True, "Progression autorisée."

        return False, "Statut maintenu (Rejeté ou en attente)."

    @staticmethod
    def get_latest_revision_status(document):
        """Retourne le statut actif basé sur la dernière révision."""
        latest = document.revisions.order_by('-date_emission').first()
        return latest.statut if latest else document.statut_actuel

    @staticmethod
    def is_document_final(document, sequence):
        """Vérifie si le document a atteint son statut final et code retour acceptant."""
        latest = document.revisions.order_by('-date_emission').first()
        if not latest:
            return False

        final_seq = [s for s in sequence if s.est_statut_final]
        is_final_status = latest.statut in [s.statut for s in final_seq]
        is_accepted = latest.code_retour in DocumentWorkflowService.CODES_RETROU_ACCEPTANTS
        return is_final_status and is_accepted

    def get_statistiques_documents(projet=None, commande=None):
        """
        Retourne un dict de statistiques documentaires.
        """
        qs = Document.objects.filter(est_archive=False)  # ⭐ CORRIGÉ

        if projet:
            qs = qs.filter(projet=projet)
        if commande:
            qs = qs.filter(commande=commande)

        return {
            'total': qs.count(),
            'en_cours': qs.filter(statut_actuel__code__in=['IFR', 'IFA']).count(),
            'finalises': qs.filter(statut_actuel__est_terminal=True).count(),
            'brouillons': qs.filter(statut_actuel__isnull=True).count(),
            'archives': qs.filter(est_archive=True).count(),  # ⭐ CORRIGÉ
            'par_classe': {
                'classe_1': qs.filter(classe__numero=1).count(),
                'classe_2': qs.filter(classe__numero=2).count(),
                'classe_3': qs.filter(classe__numero=3).count(),
            },
        }