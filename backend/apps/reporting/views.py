from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    return render(request, 'reporting/dashboard.html', {
        'page_title': 'Reporting'})

@login_required
def evm(request):
    return render(request, 'reporting/evm.html', {
        'page_title': 'EVM — Earned Value Management'})
