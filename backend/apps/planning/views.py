from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from . import services


# @login_required
# def dashboard(request):
#
#     context = {
#         "page_title": "Suivi des tâches",
#         "dashboard": services.get_dashboard(),
#     }
#
#     return render(request, "planning/dashboard.html", context)
@login_required
def dashboard(request):

    context = {
        "page_title": "Suivi des tâches",

        "dashboard": services.get_dashboard(),

        "items": services.get_gantt(),

        "retards": services.get_retards(),

        "jalons": services.get_jalons(),

        "charges": services.get_charge(),
    }

    return render(
        request,
        "planning/dashboard.html",
        context,
    )


@login_required
def par_projet(request):
    context = {
        "page_title": "Suivi des tâches par projet",
        "projets": services.get_par_projet(),
    }

    return render(request, "planning/projets.html", context)


@login_required
def par_commande(request):

    context = {
        "page_title": "Suivi des tâches par commande",
        "taches": services.get_par_commande(),
    }

    return render(request, "planning/commandes.html", context)


@login_required
def par_responsable(request):

    context = {
        "page_title": "Suivi des tâches par responsable",
        "taches": services.get_par_responsable(),
    }

    return render(request, "planning/responsables.html", context)


@login_required
def retards(request):

    context = {
        "page_title": "Tâches en retard",
        "taches": services.get_retards(),
    }

    return render(request, "planning/retards.html", context)


@login_required
def jalons(request):

    context = {
        "page_title": "Jalons",
        "taches": services.get_jalons(),
    }

    return render(request, "planning/jalons.html", context)


@login_required
def charge(request):

    context = {
        "page_title": "Tableau de charge",
        "charges": services.get_charge(),
    }

    return render(request, "planning/charge.html", context)


@login_required
def calendrier(request):

    context = {
        "page_title": "Calendrier",
        "events": services.get_calendrier_events(),
    }

    return render(request, "planning/calendrier.html", context)


@login_required
def gantt(request):

    context = {
        "page_title": "Diagramme de Gantt",
        "tasks": services.get_gantt(),
    }

    return render(request, "planning/gantt.html", context)


@login_required
def gantt_data(request):

    return JsonResponse(
        {
            "data": services.get_gantt()
        }
    )