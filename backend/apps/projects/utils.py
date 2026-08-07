"""
Utilitaires du module Projects.

Ce fichier contient des fonctions techniques
réutilisables par :
    - views.py
    - services.py
    - templates
    - exports futurs
"""


from decimal import Decimal


# ==========================================================
# FORMATAGE MONETAIRE
# ==========================================================

def format_currency(value):
    """
    Formate un montant en euros.

    Exemple:
        1250000.50
        devient
        1 250 000,50 €
    """

    if value is None:
        return "0,00 €"

    value = Decimal(value)

    return (
        f"{value:,.2f}"
        .replace(",", " ")
        .replace(".", ",")
        + " €"
    )



# ==========================================================
# FORMATAGE POURCENTAGE
# ==========================================================

def format_percent(value, decimals=1):
    """
    Formatage pourcentage.

    Exemple:
        75.234
        devient
        75,2 %
    """

    if value is None:
        return "0 %"

    return (
        f"{float(value):.{decimals}f}"
        .replace(".", ",")
        + " %"
    )



# ==========================================================
# COULEURS BOOTSTRAP
# ==========================================================

def get_status_color(statut):
    """
    Retourne une classe Bootstrap
    selon le statut projet.
    """

    return {

        "Ouvert":
            "info",

        "En cours":
            "warning",

        "En attente":
            "info",

        "Suspendu":
            "secondary",

        "Clôturé":
            "dark",

        "Finalisé":
            "success",

        "Annulé":
            "danger",

    }.get(
        statut,
        "secondary"
    )



def get_priority_color(priorite):
    """
    Retourne la couleur Bootstrap
    d'une priorité.
    """

    return {

        "Critique":
            "danger",

        "Haute":
            "warning",

        "Moyenne":
            "info",

        "Basse":
            "secondary",

    }.get(
        priorite,
        "secondary"
    )



# ==========================================================
# COULEUR AVANCEMENT
# ==========================================================

def get_progress_color(progress):
    """
    Couleur selon avancement.
    """

    if progress is None:
        return "secondary"


    progress = float(progress)


    if progress >= 70:
        return "success"


    if progress >= 30:
        return "warning"


    return "danger"



# ==========================================================
# GENERATION CODE PROJET
# ==========================================================

def generate_project_code(prefix="PRJ"):
    """
    Génère un code projet simple.

    Exemple :
        PRJ-0001

    La vérification d'unicité
    sera faite côté service.
    """

    from .models import Projet


    dernier = (
        Projet.objects
        .order_by("-id")
        .first()
    )


    if not dernier:
        numero = 1

    else:
        numero = dernier.id + 1


    return f"{prefix}-{numero:04d}"



# ==========================================================
# INDICATEUR PERFORMANCE EVM
# ==========================================================

def evm_indicator(value):
    """
    Retourne une appréciation EVM.

    SPI:
        > 1 avance
        = 1 conforme
        < 1 retard

    CPI:
        > 1 économie
        = 1 conforme
        < 1 dépassement
    """

    if value is None:
        return {
            "label": "N/A",
            "color": "secondary",
        }


    value = float(value)


    if value > 1:
        return {
            "label": "Favorable",
            "color": "success",
        }


    if value == 1:
        return {
            "label": "Conforme",
            "color": "info",
        }


    return {
        "label": "Défavorable",
        "color": "danger",
    }



# ==========================================================
# DATE UTILITAIRE
# ==========================================================

def date_range_label(date_debut, date_fin):
    """
    Retourne une période lisible.
    """

    if not date_debut and not date_fin:
        return "-"


    if date_debut and date_fin:

        return (
            f"{date_debut.strftime('%d/%m/%Y')}"
            " → "
            f"{date_fin.strftime('%d/%m/%Y')}"
        )


    if date_debut:
        return date_debut.strftime("%d/%m/%Y")


    return date_fin.strftime("%d/%m/%Y")