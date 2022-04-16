from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class Home(LoginRequiredMixin, TemplateView):

    template_name = "containers/home.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)