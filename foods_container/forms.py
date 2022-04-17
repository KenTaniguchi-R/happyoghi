from django import forms

from foods_container.models import Container

class ContainerForm(forms.Form):
    name = forms.CharField(max_length=50, label="Container Name")
    memo = forms.CharField(max_length=1000, label="Memo", widget=forms.Textarea)
    # food_name = forms.CharField(max_length=50, label="Name of Food")
    # count = forms.IntegerField(label="The number of the item")

