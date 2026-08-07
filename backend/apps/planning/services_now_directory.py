from django.db.models import Avg, Count, Sum

from apps.tasks.models import Tache


# ==========================================================
# QUERYSET DE BASE
# ==========================================================

def get_queryset():
    """
    QuerySet de base utilisé par tout le module Planning.
    """

    return (
        Tache.objects
        .select_related(
            "projet",
            "commande",
            "phase",
            "discipline",
            "responsable",
        )
    )


# ==========================================================
# DASHBOARD
# ==========================================================

def get_dashboard():

    qs = get_queryset()

    return {

        "total_taches": qs.count(),

        "en_attente":
            qs.filter(statut="En attente").count(),

        "en_cours":
            qs.filter(statut="En cours").count(),

        "terminees":
            qs.filter(statut="Terminée").count(),

        "retards":
            qs.filter(est_en_retard=True).count(),

        "jalons":
            qs.filter(est_jalon=True).count(),

        "avancement_moyen":
            qs.aggregate(
                Avg("avancement")
            )["avancement__avg"] or 0,

        "charge_totale":
            qs.aggregate(
                Sum("poids")
            )["poids__sum"] or 0,
    }


# ==========================================================
# PAR PROJET
# ==========================================================

def get_par_projet():

    return (
        get_queryset()
        .order_by(
            "projet__nom",
            "commande__code_commande",
            "date_debut_prevue",
        )
    )


# ==========================================================
# PAR COMMANDE
# ==========================================================

def get_par_commande():

    return (
        get_queryset()
        .order_by(
            "commande__code_commande",
            "date_debut_prevue",
        )
    )


# ==========================================================
# PAR RESPONSABLE
# ==========================================================

def get_par_responsable():

    return (
        get_queryset()
        .order_by(
            "responsable__last_name",
            "responsable__first_name",
            "date_fin_prevue",
        )
    )


# ==========================================================
# RETARDS
# ==========================================================

def get_retards():

    return (
        get_queryset()
        .filter(est_en_retard=True)
        .order_by("date_fin_prevue")
    )


# ==========================================================
# JALONS
# ==========================================================

def get_jalons():

    return (
        get_queryset()
        .filter(est_jalon=True)
        .order_by("date_debut_prevue")
    )


# ==========================================================
# CHARGE
# ==========================================================

def get_charge():

    return (
        get_queryset()
        .values(
            "responsable__first_name",
            "responsable__last_name",
        )
        .annotate(

            nb_taches=Count("id"),

            charge=Sum("poids"),

            avancement=Avg("avancement"),

        )
        .order_by(
            "responsable__last_name"
        )
    )


# ==========================================================
# GANTT
# ==========================================================

def get_gantt():

    return (
        get_queryset()
        .order_by(
            "projet__nom",
            "commande__code_commande",
            "date_debut_prevue",
        )
    )


# ==========================================================
# CALENDRIER
# ==========================================================

def get_calendrier():

    return (
        get_queryset()
        .exclude(
            date_debut_prevue__isnull=True
        )
        .order_by(
            "date_debut_prevue"
        )
    )