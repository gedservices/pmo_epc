from django.db.models import Avg
from django.db.models import Sum

from .base import get_queryset


def get_dashboard():
    """
    Retourne les principaux indicateurs du module Suivi des tâches.
    """

    qs = get_queryset()

    return {

        "total_taches": qs.count(),

        "taches_en_attente":
            qs.filter(statut="En attente").count(),

        "taches_en_cours":
            qs.filter(statut="En cours").count(),

        "taches_terminees":
            qs.filter(statut="Terminée").count(),

        "taches_suspendues":
            qs.filter(statut="Suspendue").count(),

        "taches_annulees":
            qs.filter(statut="Annulée").count(),

        "taches_en_retard":
            qs.filter(est_en_retard=True).count(),

        "jalons":
            qs.filter(est_jalon=True).count(),

        "avancement_moyen":
            round(
                qs.aggregate(
                    Avg("avancement")
                )["avancement__avg"] or 0,
                2,
            ),

        "charge_totale":
            qs.aggregate(
                Sum("poids")
            )["poids__sum"] or 0,

        "cout_prevu":
            qs.aggregate(
                Sum("cout_prevu")
            )["cout_prevu__sum"] or 0,

        "cout_reel":
            qs.aggregate(
                Sum("cout_reel")
            )["cout_reel__sum"] or 0,

        "planned_value":
            qs.aggregate(
                Sum("planned_value")
            )["planned_value__sum"] or 0,

        "earned_value":
            qs.aggregate(
                Sum("earned_value")
            )["earned_value__sum"] or 0,

        "actual_cost":
            qs.aggregate(
                Sum("actual_cost")
            )["actual_cost__sum"] or 0,

    }