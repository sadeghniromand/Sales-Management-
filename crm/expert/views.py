from django.contrib.auth.views import LoginView , LogoutView
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy


class ExpertLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('home')

