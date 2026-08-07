from decimal import Decimal

from django.utils import timezone


def calculate_forecast(projet):

    """
    Calcul du Forecast projet.
    """

    try:

        rule = projet.forecast_rule

    except Exception:

        rule = None



    methode = "CPI"


    facteur = Decimal("1")



    if rule:

        methode = rule.methode

        facteur = rule.facteur_performance



    budget = Decimal(
        projet.budget_prevu
    )



    if methode == "CPI":


        if projet.cpi and projet.cpi > 0:


            eac = (
                budget /
                Decimal(str(projet.cpi))
            )


        else:

            eac = budget



    elif methode == "SPI":


        if projet.spi and projet.spi > 0:


            eac = (
                budget /
                Decimal(str(projet.spi))
            )


        else:

            eac = budget




    elif methode == "HYBRID":


        cpi = Decimal(
            str(projet.cpi or 1)
        )


        spi = Decimal(
            str(projet.spi or 1)
        )


        eac = budget / (
            (cpi + spi)
            /
            Decimal("2")
        )



    else:


        eac = budget




    return {


        "methode": methode,


        "budget_initial": float(budget),


        "forecast_final": float(
            eac * facteur
        ),


        "derive": float(
            (eac * facteur) - budget
        ),


        "date_calcul": timezone.now(),


    }