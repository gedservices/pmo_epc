from .models import Conteneur


def global_context(request):
    """Injecte les données globales dans tous les templates."""
    ctx = {}
    if request.user.is_authenticated:
        ctx['conteneurs'] = Conteneur.objects.filter(actif=True).order_by('ordre')
        # Conteneur actif sélectionné (persisté en session)
        conteneur_id = request.session.get('conteneur_actif_id')
        if conteneur_id:
            try:
                ctx['conteneur_actif'] = Conteneur.objects.get(id=conteneur_id)
            except Conteneur.DoesNotExist:
                ctx['conteneur_actif'] = None
        else:
            ctx['conteneur_actif'] = Conteneur.objects.filter(
                code='RUNNING', actif=True).first()
    return ctx