from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from customer.models import Customer
from foods_container.forms import ContainerForm

from foods_container.models import Container
import requests

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
        self.container = Container.objects.get(id=self.kwargs.get("id"))
        return self.container

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        container = self.container

        # TODO: API stuff
        res = requests.get("https://api.nal.usda.gov/fdc/v1/foods/search?api_key=DEMO_KEY&query=Cheddar%20Cheese").json()
        html = "{}".format(res["foods"][0]["foodNutrients"])

        context["nutrition"] = res["foods"][0]["foodNutrients"]

        context["name"] = "data here"

        return context


class CreateContainer(LoginRequiredMixin, FormView):
    template_name = "containers/create.html"
    form_class = ContainerForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        data = form.data

        Container.objects.create(
            user_id = Customer.objects.get(id=self.request.user.id),
            name = data["name"],
            foods = {"foods": [{"name":data["food_name"], "count": data["count"]}]}
        )
        return super().form_valid(form)