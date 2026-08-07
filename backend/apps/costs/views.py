from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Cout

@login_required
def cout_list(request):
    couts = Cout.objects.select_related('projet','commande').order_by('-date_cout')
    return render(request, 'costs/list.html', {
        'page_title': 'Coûts', 'couts': couts,
    })