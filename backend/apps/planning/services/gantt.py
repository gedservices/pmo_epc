from .base import get_queryset


def get_gantt(projet=None):
    """
    Prépare les données du diagramme de Gantt.
    """

    qs = get_queryset()

    if projet:
        qs = qs.filter(projet=projet)

    data = []

    commandes = set()

    for t in qs.order_by(
        "projet__nom",
        "commande__code_commande",
        "date_debut_prevue",
    ):

        if t.commande:

            if t.commande.id not in commandes:

                commandes.add(t.commande.id)

                data.append({

                    "id": f"cmd-{t.commande.id}",

                    "text":
                        f"{t.commande.code_commande} - {t.commande.nom}",

                    "type": "project",

                    "open": True,

                })

        if t.est_en_retard:
            color = "#dc3545"

        elif t.statut == "Terminée":
            color = "#198754"

        elif t.statut == "En cours":
            color = "#fd7e14"

        else:
            color = "#6c757d"

        data.append({

            "id": t.id,

            "text": t.nom,

            "parent":
                f"cmd-{t.commande.id}" if t.commande else 0,

            "start_date":
                t.date_debut_prevue.strftime("%d-%m-%Y")
                if t.date_debut_prevue else None,

            "end_date":
                t.date_fin_prevue.strftime("%d-%m-%Y")
                if t.date_fin_prevue else None,

            "progress":
                # f"{float(t.avancement|floatformat:2)}", #/ 100,
                f"{float(t.avancement):.2f}",  # / 100

            "color": color,

            "responsable":
                str(t.responsable) if t.responsable else "",

            "phase":
                t.phase.code if t.phase else "",

            "discipline":
                t.discipline.code if t.discipline else "",

            "statut": t.statut,

            "retard": t.est_en_retard,

            "jalon": t.est_jalon,

        })

    return data