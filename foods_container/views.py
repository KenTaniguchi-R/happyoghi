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
        url = f"http://127.0.0.1:8000/detail/{self.kwargs.get('id')}"
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

        # TODO: API stuff

        #TODO: make foods list to json and
        newContainer = Container.objects.create(
            user_id = Customer.objects.get(id=self.request.user.id),
            name = data["name"],
            memo = data["memo"],
            foods = {data["food_name"]: data["count"]}
        )
        self.containerUUID = newContainer.id
        return super().form_valid(form)

class EditContainer(LoginRequiredMixin, FormView):
    template_name = "containers/edit.html"
    form_class = ContainerForm

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'id': self.containerUUID})

    def get_initial(self):
        initial = super().get_initial()
        self.container = Container.objects.get(id=self.kwargs.get("id"))

        initial["name"] = self.container.name
        foodnames = list(self.container.foods.keys())
        counter = list(self.container.foods.values())
        initial["food_name"] = foodnames[0]
        initial["count"] = counter[0]
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["container"] = self.container
        return context

    def form_valid(self, form):

        data = form.data

        # TODO: API stuff

        #TODO: make foods list to json and
        self.container.name = data["name"]
        self.container.foods = {data["food_name"]: data["count"]}
        self.container.memo = data["memo"]
        self.container.save()
        self.containerUUID = self.container.id
        return super().form_valid(form)

class DeleteContainer(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        Container.objects.get(id=self.kwargs.get("id")).delete()
        return redirect(reverse_lazy('home'))