from .base import get_queryset


def get_calendrier():
    """
    Retourne les tâches planifiées pour affichage
    sous forme de calendrier.
    """

    return (
        get_queryset()
        .exclude(date_debut_prevue__isnull=True)
        .exclude(date_fin_prevue__isnull=True)
        .order_by(
            "date_debut_prevue",
            "projet__nom",
            "commande__code_commande",
        )
    )


def get_calendrier_events():
    """
    Retourne les événements au format générique
    compatible FullCalendar.
    """

    events = []

    for t in get_calendrier():

        if t.est_en_retard:
            color = "#dc3545"
        elif t.statut == "Terminée":
            color = "#198754"
        elif t.statut == "En cours":
            color = "#fd7e14"
        else:
            color = "#0d6efd"

        events.append({

            "id": t.id,

            "title": t.nom,

            "start": t.date_debut_prevue,

            "end": t.date_fin_prevue,

            "backgroundColor": color,

            "borderColor": color,

            "extendedProps": {

                "projet": t.projet.nom,

                "commande":
                    t.commande.code_commande if t.commande else "",

                "responsable":
                    str(t.responsable) if t.responsable else "",

                "statut": t.statut,

                "avancement": float(t.avancement),

            }

        })

    return events