from datetime import timedelta
from decimal import Decimal

from django.utils import timezone

from .models import ProjetCurvePoint



def generate_periods(
    date_debut,
    date_fin,
    granularite="MONTH"
):
    """
    Génère les périodes de calcul de la courbe S.
    """

    periods = []


    current = date_debut


    if granularite == "DAY":

        step = timedelta(days=1)


    elif granularite == "WEEK":

        step = timedelta(days=7)


    elif granularite == "MONTH":

        step = timedelta(days=30)


    elif granularite == "QUARTER":

        step = timedelta(days=90)


    elif granularite == "SEMESTER":

        step = timedelta(days=180)


    elif granularite == "YEAR":

        step = timedelta(days=365)


    else:

        step = timedelta(days=30)



    while current <= date_fin:

        periods.append(current)

        current += step



    return periods





def generate_planned_curve(projet, granularite="MONTH"):
    """
    Génère la courbe prévisionnelle.

    Hypothèse initiale :
    progression linéaire entre début et fin projet.
    """

    if not projet.date_debut_prevue:
        return []


    if not projet.date_fin_prevue:
        return []



    periods = generate_periods(
        projet.date_debut_prevue,
        projet.date_fin_prevue,
        granularite
    )


    total_budget = Decimal(
        projet.budget_prevu
    )


    total_periods = len(periods)


    points = []



    for index, date in enumerate(periods, start=1):

        progression = Decimal(index) / Decimal(total_periods)


        pv = total_budget * progression



        points.append({

            "date": date,

            "planned_value": round(
                pv,
                2
            )

        })


    return points






def get_scurve_data(projet, granularite="MONTH"):

    """
    Retourne les données utilisables par Chart.js.
    """


    planned = generate_planned_curve(
        projet,
        granularite
    )


    actual_points = ProjetCurvePoint.objects.filter(
        projet=projet,
        granularite=granularite
    ).order_by(
        "date"
    )



    labels = []


    planned_values = []

    earned_values = []

    actual_costs = []

    forecasts = []



    for p in planned:


        labels.append(
            p["date"].strftime("%d/%m/%Y")
        )


        planned_values.append(
            float(
                p["planned_value"]
            )
        )


    actual_dict = {

        p.date.strftime("%d/%m/%Y"):

        p

        for p in actual_points

    }



    for label in labels:


        point = actual_dict.get(label)



        if point:


            earned_values.append(
                float(point.earned_value)
            )


            actual_costs.append(
                float(point.actual_cost)
            )


            forecasts.append(
                float(point.forecast_value)
            )


        else:


            earned_values.append(0)


            actual_costs.append(0)


            forecasts.append(0)



    return {


        "labels": labels,


        "planned": planned_values,


        "earned": earned_values,


        "actual": actual_costs,


        "forecast": forecasts,

    }