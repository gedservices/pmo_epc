from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Risque
from .forms import RisqueForm
from apps.projects.models import Projet


@login_required
def risque_list(request):
    qs = Risque.objects.select_related('projet', 'commande', 'responsable')

    projet_id = request.GET.get('projet', '')
    statut    = request.GET.get('statut', '')
    search    = request.GET.get('q', '').strip()

    if projet_id:
        qs = qs.filter(projet_id=projet_id)
    if statut:
        qs = qs.filter(statut=statut)
    if search:
        qs = qs.filter(titre__icontains=search)

    # Tri criticité décroissante
    risques_tries = sorted(qs, key=lambda r: r.criticite, reverse=True)
    paginator     = Paginator(risques_tries, 25)
    page          = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'risks/list.html', {
        'page_title':  'Risques',
        'risques':     page,
        'projets':     Projet.objects.filter(est_generique=False),
        'filtre_projet': projet_id,
        'filtre_statut': statut,
        'search':        search,
        'statut_choices': Risque.STATUT_CHOICES,
    })


@login_required
def matrice(request):
    projet_id = request.GET.get('projet', '')
    qs = Risque.objects.select_related('projet')
    if projet_id:
        qs = qs.filter(projet_id=projet_id)

    # Construction matrice 5x5
    matrice_data = {}
    for r in qs:
        key = (r.probabilite, r.impact)
        if key not in matrice_data:
            matrice_data[key] = []
        matrice_data[key].append(r)

    return render(request, 'risks/matrix.html', {
        'page_title':   'Matrice des Risques',
        'risques':      qs,
        'matrice_data': matrice_data,
        'projets':      Projet.objects.filter(est_generique=False),
        'filtre_projet': projet_id,
        'range_5':      range(1, 6),
    })


@login_required
def risque_create(request):
    if request.method == 'POST':
        form = RisqueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Risque enregistré.")
            return redirect('risks:list')
    else:
        form = RisqueForm()
    return render(request, 'risks/form.html', {
        'page_title': 'Nouveau Risque',
        'form': form, 'action': 'create',
    })


@login_required
def risque_edit(request, pk):
    risque = get_object_or_404(Risque, pk=pk)
    if request.method == 'POST':
        form = RisqueForm(request.POST, instance=risque)
        if form.is_valid():
            form.save()
            messages.success(request, "Risque mis à jour.")
            return redirect('risks:list')
    else:
        form = RisqueForm(instance=risque)
    return render(request, 'risks/form.html', {
        'page_title': f'Modifier — {risque.titre}',
        'form': form, 'risque': risque, 'action': 'edit',
    })


@login_required
def risque_delete(request, pk):
    risque = get_object_or_404(Risque, pk=pk)
    if request.method == 'POST':
        risque.delete()
        messages.success(request, "Risque supprimé.")
        return redirect('risks:list')
    return render(request, 'risks/confirm_delete.html', {
        'page_title': 'Supprimer Risque', 'risque': risque,
    })
