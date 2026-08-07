from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProjetForm
from .models import MigrationConteneurLog, Projet
from apps.core_ref.models import Conteneur
from django.shortcuts import redirect, render
import traceback

from django.db import DatabaseError

import logging

logger = logging.getLogger(__name__)

# ==========================================================
# LISTE DES PROJETS
# ==========================================================

@login_required
def projet_list(request):
    """
    Liste des projets avec recherche, filtres et statistiques.
    """

    projets = (
        Projet.objects
        .select_related(
            "conteneur",
            "responsable",
            "entite",
            "pays",
            "site",
            "secteur",
        )
        # .all()
        # .filter(
        #     conteneur__code__ne="DELETED"     # "__ne" (not equal) non supporté par Django
        # )
        .exclude(
            conteneur__code="DELETED"
        )
    )

    search = request.GET.get("q", "").strip()
    filtre_statut = request.GET.get("statut", "")
    filtre_priorite = request.GET.get("priorite", "")

    if search:
        projets = projets.filter(
            Q(code__icontains=search)
            | Q(nom__icontains=search)
            | Q(description__icontains=search)
        )

    if filtre_statut:
        projets = projets.filter(statut=filtre_statut)

    if filtre_priorite:
        projets = projets.filter(priorite=filtre_priorite)

    contexte = {
        "projets": projets,
        "nb_total": projets.count(),
        "nb_retard": sum(1 for p in projets if p.est_en_retard),

        "search": search,
        "filtre_statut": filtre_statut,
        "filtre_priorite": filtre_priorite,

        "statut_choices": Projet.STATUT_CHOICES,
        "priorite_choices": Projet.PRIORITE_CHOICES,
    }

    return render(
        request,
        "projects/list.html",
        contexte,
    )


# ==========================================================
# DETAIL
# ==========================================================

@login_required
def projet_detail(request, pk):
    """
    Affichage d'un projet.
    """

    projet = get_object_or_404(
        Projet.objects.select_related(
            "conteneur",
            "responsable",
            "entite",
            "pays",
            "site",
            "secteur",
            "cree_par",
            "modifie_par",
        ),
        pk=pk,
    )

    contexte = {
        "projet": projet,
    }

    return render(
        request,
        "projects/detail.html",
        contexte,
    )




# ==========================================================
# CREATION
# ==========================================================

@login_required
def projet_create(request):

    if request.method == "POST":

        form = ProjetForm(request.POST)

        if form.is_valid():

            try:

                projet = form.save(commit=False)

                projet.cree_par = request.user
                projet.modifie_par = request.user

                projet.save()

                form.save_m2m()

                messages.success(
                    request,
                    "Le projet a été créé avec succès.",
                )

                return redirect(
                    "projects:detail",
                    pk=projet.pk,
                )

            except Exception as e:

                print("\n" + "=" * 80)
                print("ERREUR LORS DE LA CREATION DU PROJET")
                traceback.print_exc()
                print(f"Message : {e}")
                print("=" * 80 + "\n")

                messages.error(
                    request,
                    "Une erreur système est survenue lors de la création du projet."
                )


        else:

            print("=" * 80)
            print("ERREURS DU FORMULAIRE")

            for field, errors in form.errors.items():
                print(f"{field} :")
                for error in errors:
                    print(f"   - {error}")

            print("=" * 80)

            # Message générique
            messages.error(
                request,
                "Le projet n'a pas pu être créé. Veuillez corriger les erreurs du formulaire."
            )

            # Message détaillé
            erreurs = []

            for field, errors in form.errors.items():

                libelle = form.fields[field].label if field in form.fields else field

                for error in errors:
                    erreurs.append(f"{libelle} : {error}")

            messages.error(
                request,
                "Détail : " + " | ".join(erreurs)
            )

            print(request.POST)

    else:

        form = ProjetForm()

    return render(
        request,
        "projects/form.html",
        {
            "form": form,
            "mode": "create",
            "page_title": "Nouveau projet",
        },
    )



# ==========================================================
# MODIFICATION
# ==========================================================

@login_required
def projet_edit(request, pk):

    projet = get_object_or_404(
        Projet,
        pk=pk,
    )

    if request.method == "POST":

        form = ProjetForm(
            request.POST,
            instance=projet,
        )

        if form.is_valid():

            projet = form.save(commit=False)

            projet.modifie_par = request.user

            projet.save()

            form.save_m2m()

            messages.success(
                request,
                "Le projet a été modifié avec succès.",
            )

            return redirect(
                "projects:detail",
                pk=projet.pk,
            )

    else:

        form = ProjetForm(instance=projet)

    return render(
        request,
        "projects/form.html",
        {
            "form": form,
            "mode": "edit",
            "projet": projet,
            "page_title": "Modification du projet",
        },
    )



# ==========================================================
# MIGRATION DE CONTENEUR
# ==========================================================

@login_required
def projet_migrate(request, pk):

    projet = get_object_or_404(
        Projet,
        pk=pk,
    )

    conteneurs = (
        Conteneur.objects
        .exclude(pk=projet.conteneur.pk)
        .order_by("libelle")
    )

    if request.method == "POST":

        nouveau_conteneur = get_object_or_404(
            Conteneur,
            pk=request.POST.get("conteneur"),
        )

        commentaire = request.POST.get(
            "commentaire",
            "",
        )

        ancien = projet.conteneur

        projet.conteneur = nouveau_conteneur
        projet.modifie_par = request.user

        projet.save()

        # MigrationConteneurLog.objects.create(
        #     projet=projet,
        #     conteneur_source=ancien,
        #     conteneur_cible=nouveau_conteneur,
        #     migre_par=request.user,
        #     commentaire=commentaire,
        # )

        MigrationConteneurLog.objects.create(
            projet=projet,
            conteneur_source=ancien,
            conteneur_cible=nouveau_conteneur,
            migre_par=request.user,
            commentaire=commentaire,
            type_operation="MIGRATION",
        )

        messages.success(
            request,
            "Migration réalisée avec succès.",
        )

        return redirect(
            "projects:detail",
            pk=projet.pk,
        )

    return render(
        request,
        "projects/migrate.html",
        {
            "projet": projet,
            "conteneurs": conteneurs,
        },
    )





# ==========================================================
# SUPPRESSION = # MIGRATION VERS CONTENEUR "DELETED"
# ==========================================================
@login_required
def projet_delete(request, pk):

    projet = get_object_or_404(Projet, pk=pk)

    if request.method == "POST":

        try:

            corbeille = Conteneur.objects.get(code="DELETED")

        except Conteneur.DoesNotExist:

            messages.error(
                request,
                "Le conteneur 'DELETED' est introuvable."
            )

            return redirect(
                "projects:detail",
                pk=projet.pk,
            )

        ancien = projet.conteneur

        projet.conteneur = corbeille
        projet.modifie_par = request.user
        projet.save()

        # MigrationConteneurLog.objects.create(
        #     projet=projet,
        #     conteneur_source=ancien,
        #     conteneur_cible=corbeille,
        #     migre_par=request.user,
        #     commentaire="Suppression logique du projet.",
        # )

        MigrationConteneurLog.objects.create(
            projet=projet,
            conteneur_source=ancien,
            conteneur_cible=corbeille,
            migre_par=request.user,
            commentaire="Déplacement vers la corbeille",
            type_operation="DELETE",
        )

        messages.success(
            request,
            "Le projet a été déplacé dans la corbeille."
        )

        return redirect("projects:list")

    return render(
        request,
        "projects/delete.html",
        {
            "projet": projet,
        },
    )


# ===================================================================
# CORBEILLE = PROJETS EFFECTICEMENT MIGRES  VERS CONTENEUR "DELETED"
# ===================================================================
@login_required
def projet_trash(request):

    projets = (
        Projet.objects
        .select_related(
            "conteneur",
            "responsable",
            "entite",
            "pays",
            "site",
            "secteur",
        )
        .filter(
            conteneur__code="DELETED"
        )
    )

    return render(
        request,
        "projects/trash.html",
        {
            "projets": projets,
        },
    )



# S-CURVVE STUFF

def projet_scurve(request, pk):

    projet = get_object_or_404(
        Projet,
        pk=pk
    )


    data = generate_scurve_data(
        projet
    )


    forecast = calculate_forecast(
        projet
    )


    context = {

        "projet": projet,

        "curve_data": data,

        "forecast": forecast,

    }


    return render(
        request,
        "projects/scurve.html",
        context
    )