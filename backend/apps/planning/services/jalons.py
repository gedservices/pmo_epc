from .base import get_queryset


def get_jalons():
    """
    Retourne les jalons.
    """

    return (
        get_queryset()
        .filter(est_jalon=True)
        .order_by(
            "date_debut_prevue",
            "projet__nom",
        )
    )