from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView

from customer.forms import LoginForm, SignUpForm


class Login(LoginView):
    form_class = LoginForm
    template_name = 'user_auth/login.html'

class SignUp(CreateView):
    template_name = "user_auth/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy('home')

class Logout(LogoutView):

    def get(self, request, *args, **kwargs):
        return redirect(reverse_lazy('login'))