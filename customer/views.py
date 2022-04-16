from django.shortcuts import render
from django.contrib.auth.views import LoginView

from customer.forms import LoginForm


class Login(LoginView):
    form_class = LoginForm
    template_name = 'user_auth/login.html'