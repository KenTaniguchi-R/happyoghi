from attr import fields
from django import forms

from foods_container.models import Container

class ContainerForm(forms.Form):
    name = forms.CharField(max_length=50, label="Container Name")
    food_name = forms.CharField(max_length=50, label="Name of Food")
    count = forms.IntegerField(label="The number of the item")

