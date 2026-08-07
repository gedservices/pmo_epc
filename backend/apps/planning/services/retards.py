from .base import get_queryset


def get_retards():
    """
    Retourne les tâches en retard.
    """

    return (
        get_queryset()
        .filter(est_en_retard=True)
        .order_by(
            "date_fin_prevue",
            "projet__nom",
            "commande__code_commande",
        )
    )