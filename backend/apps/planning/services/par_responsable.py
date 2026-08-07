from .base import get_queryset


def get_par_responsable(responsable=None):
    """
    Retourne les tâches regroupées par responsable.
    """

    qs = get_queryset()

    if responsable:
        qs = qs.filter(responsable=responsable)

    return (
        qs
        .order_by(
            "responsable__last_name",
            "responsable__first_name",
            "date_fin_prevue",
            "nom",
        )
    )