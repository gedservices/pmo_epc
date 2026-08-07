"""
Planning Project — moteur de planification (baselines, dépendances, chemin critique).
Phase 0 : stubs pour que `check` passe ; à implémenter Phase 2.
"""
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render


@login_required
def dashboard(request):
    return render(request, "planning_project/dashboard.html", {})


@login_required
def planning(request):
    return render(request, "planning_project/planning.html", {})


@login_required
def versions(request):
    return render(request, "planning_project/versions.html", {})


@login_required
def baseline(request):
    return render(request, "planning_project/baseline.html", {})


@login_required
def dependencies(request):
    return render(request, "planning_project/dependencies.html", {})


@login_required
def constraints(request):
    return render(request, "planning_project/constraints.html", {})


@login_required
def resources(request):
    return render(request, "planning_project/resources.html", {})


@login_required
def calendars(request):
    return render(request, "planning_project/calendars.html", {})


@login_required
def critical_path(request):
    return render(request, "planning_project/critical_path.html", {})


@login_required
def gantt_data(request):
    return JsonResponse({"tasks": [], "links": []})
