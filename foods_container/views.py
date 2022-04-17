from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from customer.models import Customer
from foods_container.forms import ContainerForm

from foods_container.models import Container
import requests

from io import BytesIO
import qrcode, base64

# Create your views here.

def get_base_encoding(url):
    buffer = BytesIO()
    qr = qrcode.make(url)
    qr.save(buffer, format="png")
    return base64.b64encode(buffer.getvalue()).decode().replace("'", "")

class Home(LoginRequiredMixin, ListView):
    template_name = "containers/home.html"

    def get_queryset(self):
        q_word = self.request.GET.get('query')
        if q_word:
            return Container.objects.filter(
                Q(foods__icontains=q_word) | Q(memo__icontains=q_word),
                user_id=self.request.user)
        return Container.objects.filter(user_id=self.request.user)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ContainerDetail(DetailView):

    model = Container
    template_name = "containers/detail.html"

    def get_object(self, queryset=None):
        self.container = Container.objects.get(id=self.kwargs.get("id"))
        return self.container

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        url = f"https://happyoghi.herokuapp.com/detail/{self.kwargs.get('id')}"
        qrcode = get_base_encoding(url)
        context["qrcode"] = qrcode
        return context


class CreateContainer(LoginRequiredMixin, FormView):
    template_name = "containers/create.html"
    form_class = ContainerForm

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'id': self.containerUUID})

    def form_valid(self, form):
        data = form.data

        foods = {"foods": []}
        foods_id = 0
        while "food_{}".format(foods_id) in data.keys():
            foods["foods"].append({"name":data["food_{}".format(foods_id)], "count": data["count_{}".format(foods_id)]})
            foods_id += 1

        # TODO: API stuff
        for index, food_item in enumerate(foods["foods"]):
            food_name = food_item["name"]
            res = requests.get("https://api.nal.usda.gov/fdc/v1/foods/search?api_key=DEMO_KEY&query={}".format(food_name)).json()
            if res["totalHits"]:
                res["foods"] = res["foods"][0]
                foods["foods"][index]["nutritions"] = res
            else:
                foods["foods"][index]["nutritions"] = {}

        #TODO: make foods list to json and
        newContainer = Container.objects.create(
            user_id = Customer.objects.get(id=self.request.user.id),
            name = data["name"],
            foods = foods,
            memo = data["memo"]
        )
        self.containerUUID = newContainer.id
        return super().form_valid(form)

class EditContainer(LoginRequiredMixin, FormView):
    template_name = "containers/edit.html"
    form_class = ContainerForm
    foods = {}

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'id': self.containerUUID})

    def get_initial(self):
        initial = super().get_initial()
        self.container = Container.objects.get(id=self.kwargs.get("id"))

        initial["name"] = self.container.name
        initial["memo"] = self.container.memo
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for i, food in enumerate(self.container.foods["foods"]):
            self.foods[food["name"]] = food["count"]
        context["foods"] = self.foods
        context["container_name"] = self.container.name
        return context

    def form_valid(self, form):

        data = form.data

        # TODO: API stuff
        foods = {"foods": []}
        foods_id = 0
        while "food_{}".format(foods_id) in data.keys():
            foods["foods"].append({"name":data["food_{}".format(foods_id)], "count": data["count_{}".format(foods_id)]})
            foods_id += 1

        for index, food_item in enumerate(foods["foods"]):
            food_name = food_item["name"]
            if len(self.foods.keys())>index and food_name == list(self.foods.keys())[index]:
                foods["foods"][index]["nutritions"] = self.container.foods["foods"][index]["nutritions"]
            else:
                res = requests.get("https://api.nal.usda.gov/fdc/v1/foods/search?api_key=DEMO_KEY&query={}".format(food_name)).json()
                if res["totalHits"]:
                    res["foods"] = res["foods"][0]
                    foods["foods"][index]["nutritions"] = res
                else:
                    foods["foods"][index]["nutritions"] = {}

        #TODO: make foods list to json and
        self.container.name = data["name"]
        self.container.foods = foods
        self.container.memo = data["memo"]
        self.container.save()
        self.containerUUID = self.container.id
        return super().form_valid(form)

class DeleteContainer(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        Container.objects.get(id=self.kwargs.get("id")).delete()
        return redirect(reverse_lazy('home'))