from django.shortcuts import render

# Create your views here.

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm


class LoginView(auth_views.LoginView):
    form_class    = LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        remember = form.cleaned_data.get('remember_me')
        if not remember:
            self.request.session.set_expiry(0)
        return super().form_valid(form)


class LogoutView(auth_views.LogoutView):
    next_page = '/auth/login/'


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {
        'page_title': 'Mon Profil'
    })
