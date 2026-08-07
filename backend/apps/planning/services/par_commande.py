from .base import get_queryset


def get_par_commande(commande=None):
    """
    Retourne les tâches regroupées par commande.
    """

    qs = get_queryset()

    if commande:
        qs = qs.filter(commande=commande)

    return (
        qs
        .order_by(
            "commande__code_commande",
            "date_debut_prevue",
            "nom",
        )
    )