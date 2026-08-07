from collections import OrderedDict

from django.db.models import Avg

from .base import get_queryset


def get_par_projet(projet=None):
    """
    Retourne les données de planning regroupées par Projet puis Commande.
    """

    qs = get_queryset().select_related(
        "projet",
        "commande",
        "responsable",
        "phase",
        "discipline",
    )

    if projet:
        qs = qs.filter(projet=projet)

    qs = qs.order_by(
        "projet__nom",
        "commande__code_commande",
        "date_debut_prevue",
        "nom",
    )

    projets = OrderedDict()

    for task in qs:

        projet_id = task.projet.id

        if projet_id not in projets:

            projets[projet_id] = {

                "projet": task.projet,

                "commandes": OrderedDict(),

                "nb_taches": 0,

                "nb_commandes": 0,

                "nb_retards": 0,

                "avancement_total": 0,
            }

        p = projets[projet_id]

        p["nb_taches"] += 1

        p["avancement_total"] += task.avancement or 0

        if task.est_en_retard:
            p["nb_retards"] += 1

        cmd = task.commande

        cmd_id = cmd.id if cmd else 0

        if cmd_id not in p["commandes"]:

            p["commandes"][cmd_id] = {

                "commande": cmd,

                "taches": [],
            }

            p["nb_commandes"] += 1

        p["commandes"][cmd_id]["taches"].append(task)

    resultat = []

    for p in projets.values():

        if p["nb_taches"]:

            p["avancement"] = round(
                p["avancement_total"] / p["nb_taches"],
                1,
            )

        else:

            p["avancement"] = 0

        p["commandes"] = list(
            p["commandes"].values()
        )

        del p["avancement_total"]

        resultat.append(p)

    return resultat