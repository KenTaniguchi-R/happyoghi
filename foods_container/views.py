from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from foods_container.models import Container

# Create your views here.

class Home(LoginRequiredMixin, ListView):
    template_name = "containers/home.html"

    def get_queryset(self):

        return Container.objects.filter(user_id=self.request.user)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ContainerDetail(LoginRequiredMixin, DetailView):

    model = Container
    template_name = "containers/detail.html"

    def get_object(self, queryset=None):
        return Container.objects.get(id=self.kwargs.get("id"))
