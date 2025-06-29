from django.contrib import auth
from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('recipe:index')
    template_name = 'users/signup.html'


def logout(request):
    auth.logout(request)
    return render(request, 'users/logged_out.html')