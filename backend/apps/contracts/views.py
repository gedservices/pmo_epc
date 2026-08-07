from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Commande
from .forms import CommandeForm
from .filters import CommandeFilter  # ⭐ NOUVEAU


@login_required
def commande_list(request):
    """
    Liste des commandes avec filtres et pagination.
    """
    # Queryset de base
    queryset = Commande.objects.select_related(
        "projet",
        "responsable",
        "phase",
        "entite_contractor",
    ).order_by(
        "projet",
        "code_commande"
    )

    # ⭐ NOUVEAU : Appliquer les filtres
    filterset = CommandeFilter(request.GET, queryset=queryset)
    commandes_filtrees = filterset.qs

    # ⭐ NOUVEAU : Statistiques
    nb_total = commandes_filtrees.count()

    # ⭐ NOUVEAU : Pagination
    paginator = Paginator(commandes_filtrees, 25)
    page_number = request.GET.get('page', 1)
    commandes = paginator.get_page(page_number)

    # ⭐ NOUVEAU : Préparer les choix pour les filtres
    statut_choices = Commande.STATUT_CHOICES if hasattr(Commande, 'STATUT_CHOICES') else []
    priorite_choices = Commande.PRIORITE_CHOICES if hasattr(Commande, 'PRIORITE_CHOICES') else []

    # ⭐ NOUVEAU : Récupérer les filtres actifs
    search = request.GET.get('q', '')
    filtre_statut = request.GET.get('statut', '')
    filtre_priorite = request.GET.get('priorite', '')
    filtre_phase = request.GET.get('phase', '')
    filtre_projet = request.GET.get('projet', '')

    return render(
        request,
        "contracts/list.html",
        {
            "commandes": commandes,
            "filterset": filterset,  # ⭐ NOUVEAU
            "nb_total": nb_total,  # ⭐ NOUVEAU
            "statut_choices": statut_choices,  # ⭐ NOUVEAU
            "priorite_choices": priorite_choices,  # ⭐ NOUVEAU
            "search": search,  # ⭐ NOUVEAU
            "filtre_statut": filtre_statut,  # ⭐ NOUVEAU
            "filtre_priorite": filtre_priorite,  # ⭐ NOUVEAU
            "filtre_phase": filtre_phase,  # ⭐ NOUVEAU
            "filtre_projet": filtre_projet,  # ⭐ NOUVEAU
            "page_title": "Commandes",
            "create_url": "/contracts/create/",
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

            messages.success(
                request,
                "La commande a été créée avec succès."
            )

            return redirect(
                "contracts:detail",
                pk=obj.pk
            )

    else:

        form = CommandeForm()

    return render(
        request,
        "contracts/form.html",
        {
            "form": form,
            "page_title": "Nouvelle commande",
            "submit_label": "Créer",
        },
    )


@login_required
def commande_detail(request, pk):

    commande = get_object_or_404(
        Commande.objects.select_related(
            "projet",
            "responsable",
            "phase",
            "pays",
            "site",
            "secteur",
            "entite_contractor",
        ),
        pk=pk
    )

    return render(
        request,
        "contracts/detail.html",
        {
            "commande": commande,
            "page_title": commande.code_commande,
        },
    )


@login_required
def commande_update(request, pk):

    commande = get_object_or_404(
        Commande,
        pk=pk
    )

    if request.method == "POST":

        form = CommandeForm(
            request.POST,
            instance=commande
        )

        if form.is_valid():

            obj = form.save(commit=False)

            obj.modifie_par = request.user

            obj.save()

            messages.success(
                request,
                "La commande a été modifiée."
            )

            return redirect(
                "contracts:detail",
                pk=obj.pk
            )

    else:

        form = CommandeForm(
            instance=commande
        )

    return render(
        request,
        "contracts/form.html",
        {
            "form": form,
            "page_title": "Modifier la commande",
            "submit_label": "Enregistrer",
        },
    )


@login_required
def commande_delete(request, pk):

    commande = get_object_or_404(
        Commande,
        pk=pk
    )

    if request.method == "POST":

        code = commande.code_commande

        commande.delete()

        messages.success(
            request,
            f"La commande {code} a été supprimée."
        )

        return redirect(
            "contracts:list"
        )

    return render(
        request,
        "contracts/confirm_delete.html",
        {
            "commande": commande,
            "page_title": "Supprimer la commande",
        },
    )