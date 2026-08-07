from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Commande

@login_required
def commande_list(request):
    commandes = Commande.objects.select_related(
        'projet', 'phase', 'responsable').order_by('code_commande')
    return render(request, 'contracts/list.html', {
        'page_title': 'Commandes',
        'commandes':  commandes,
    })
