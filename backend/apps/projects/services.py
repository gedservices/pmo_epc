"""
Services métier du module Projects.

Ce fichier contient toute la logique métier indépendante
des vues et des templates.

Les vues doivent uniquement :
    - récupérer les paramètres
    - appeler un service
    - retourner une réponse

Toutes les règles PMO doivent être centralisées ici.
"""

from decimal import Decimal

from django.db.models import Count, Sum

from .models import Projet


# ==========================================================
# TABLEAU DE BORD
# ==========================================================

def get_dashboard_stats():
    """
    Statistiques générales des projets.
    """

    projets = Projet.objects.all()

    stats = {
        "nb_total": projets.count(),
        "nb_ouverts": projets.filter(statut="Ouvert").count(),
        "nb_en_cours": projets.filter(statut="En cours").count(),
        "nb_suspendus": projets.filter(statut="Suspendu").count(),
        "nb_finalises": projets.filter(statut="Finalisé").count(),
        "nb_clotures": projets.filter(statut="Clôturé").count(),
        "nb_annules": projets.filter(statut="Annulé").count(),
        "nb_retard": sum(1 for p in projets if p.est_en_retard),
    }

    return stats


# ==========================================================
# BUDGET
# ==========================================================

def get_budget_stats():
    """
    Agrégats budgétaires.
    """

    projets = Projet.objects.all()

    total_prevu = (
        projets.aggregate(
            total=Sum("budget_prevu")
        )["total"]
        or Decimal("0")
    )

    total_reel = (
        projets.aggregate(
            total=Sum("budget_reel")
        )["total"]
        or Decimal("0")
    )

    derive = total_reel - total_prevu

    taux = 0

    if total_prevu > 0:
        taux = round(
            float(total_reel / total_prevu * 100),
            1,
        )

    return {
        "budget_prevu": total_prevu,
        "budget_reel": total_reel,
        "derive_budget": derive,
        "taux_consommation": taux,
    }


# ==========================================================
# EVM
# ==========================================================

def get_evm_stats():
    """
    Statistiques Earned Value.
    """

    projets = Projet.objects.all()

    pv = (
        projets.aggregate(
            total=Sum("planned_value")
        )["total"]
        or Decimal("0")
    )

    ev = (
        projets.aggregate(
            total=Sum("earned_value")
        )["total"]
        or Decimal("0")
    )

    ac = (
        projets.aggregate(
            total=Sum("actual_cost")
        )["total"]
        or Decimal("0")
    )

    spi = None
    cpi = None

    if pv > 0:
        spi = round(float(ev / pv), 3)

    if ac > 0:
        cpi = round(float(ev / ac), 3)

    return {
        "planned_value": pv,
        "earned_value": ev,
        "actual_cost": ac,
        "spi": spi,
        "cpi": cpi,
    }


# ==========================================================
# RECHERCHE
# ==========================================================

def search_projects(queryset, texte):
    """
    Recherche plein texte.
    """

    from django.db.models import Q

    if not texte:
        return queryset

    return queryset.filter(
        Q(code__icontains=texte)
        | Q(nom__icontains=texte)
        | Q(description__icontains=texte)
    )


# ==========================================================
# STATISTIQUES D'UN PROJET
# ==========================================================

def get_project_stats(projet):
    """
    Toutes les statistiques utiles à la fiche projet.
    """

    return {

        "est_en_retard": projet.est_en_retard,

        "derive_budget": projet.derive_budget,

        "taux_consommation": projet.taux_consommation,

        "spi": projet.spi,

        "cpi": projet.cpi,

        "progression": projet.progression_calculee,

    }


# ==========================================================
# RAFRAICHISSEMENT
# ==========================================================

def refresh_project(projet):
    """
    Recalcule les indicateurs du projet.
    """

    projet.recalculer_progression()

    projet.refresh_from_db()

    return projet


# ==========================================================
# REPARTITION PAR STATUT
# ==========================================================

def get_statut_distribution():
    """
    Répartition des projets par statut.
    """

    return (
        Projet.objects
        .values("statut")
        .annotate(total=Count("id"))
        .order_by("statut")
    )


# ==========================================================
# REPARTITION PAR PRIORITE
# ==========================================================

def get_priorite_distribution():
    """
    Répartition des projets par priorité.
    """

    return (
        Projet.objects
        .values("priorite")
        .annotate(total=Count("id"))
        .order_by("priorite")
    )