from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Commande
from .forms import CommandeForm


@login_required
def commande_list(request):

    commandes = Commande.objects.select_related(
        "projet",
        "responsable",
        "phase",
    )

    return render(
        request,
        "contracts/list.html",
        {
            "commandes": commandes,
        },
    )


@login_required
def commande_create(request):

    if request.method == "POST":

        form = CommandeForm(request.POST)

        if form.is_valid():

            obj = form.save(commit=False)

            obj.cree_par = request.user
            obj.modifie_par = request.user

            obj.save()

            return redirect("contracts:list")

    else:

        form = CommandeForm()

    return render(
        request,
        "contracts/form.html",
        {
            "form": form,
            "title": "Nouvelle commande",
        },
    )


@login_required
def commande_detail(request, pk):

    commande = get_object_or_404(Commande, pk=pk)

    return render(
        request,
        "contracts/detail.html",
        {
            "commande": commande,
        },
    )


@login_required
def commande_update(request, pk):

    commande = get_object_or_404(Commande, pk=pk)

    if request.method == "POST":

        form = CommandeForm(request.POST, instance=commande)

        if form.is_valid():

            obj = form.save(commit=False)

            obj.modifie_par = request.user

            obj.save()

            return redirect("contracts:list")

    else:

        form = CommandeForm(instance=commande)

    return render(
        request,
        "contracts/form.html",
        {
            "form": form,
            "title": "Modifier la commande",
        },
    )


@login_required
def commande_delete(request, pk):

    commande = get_object_or_404(Commande, pk=pk)

    if request.method == "POST":

        commande.delete()

        return redirect("contracts:list")

    return render(
        request,
        "contracts/confirm_delete.html",
        {
            "commande": commande,
        },
    )