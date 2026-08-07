from apps.tasks.models import Tache


def get_queryset():
    """
    QuerySet de base utilisé par l'ensemble du module Planning.
    Toutes les vues et tous les services partent de cette requête.
    """

    return (
        Tache.objects
        .select_related(
            "projet",
            "commande",
            "phase",
            "discipline",
            "responsable",
        )
    )