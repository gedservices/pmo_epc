from django.db.models import Avg
from django.db.models import Count
from django.db.models import Sum

from .base import get_queryset


def get_charge():
    """
    Charge par responsable.
    """

    return (

        get_queryset()

        .values(

            "responsable__id",
            "responsable__first_name",
            "responsable__last_name",

        )

        .annotate(

            nb_taches=Count("id"),

            charge=Sum("poids"),

            avancement=Avg("avancement"),

            cout_prevu=Sum("cout_prevu"),

            cout_reel=Sum("cout_reel"),

        )

        .order_by(

            "responsable__last_name",
            "responsable__first_name",

        )

    )