from django.views import View
from django.views.generic.base import TemplateView
from django.shortcuts import render

# Create your views here.

class Home(TemplateView):

    template_name = "containers/home.html"
