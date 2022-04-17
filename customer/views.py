from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView

from customer.forms import LoginForm, SignUpForm


class LP(TemplateView):
    template_name= 'user_auth/LP.html'


class Login(LoginView):
    form_class = LoginForm
    template_name = 'user_auth/login.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('home'))
        return super().get(request, *args, **kwargs)

class SignUp(CreateView):
    template_name = "user_auth/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy('home')

class Logout(LogoutView):

    def get(self, request, *args, **kwargs):
        return redirect(reverse_lazy('login'))