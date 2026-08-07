from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Conteneur


@login_required
def index(request):
    return render(request, 'core_ref/index.html', {
        'page_title': 'Référentiels'
    })


@login_required
def set_conteneur(request, pk):
    """Change le conteneur actif en session."""
    conteneur = get_object_or_404(Conteneur, pk=pk)
    request.session['conteneur_actif_id'] = conteneur.id
    next_url = request.GET.get('next', '/dashboard/')
    return redirect(next_url)
