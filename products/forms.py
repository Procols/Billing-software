from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "quantity", "unit_price"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control"}),
        }


class UpdateQuantityForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["quantity"]
        widgets = {
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
        }
