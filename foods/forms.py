from django import forms
from .models import FoodAndDrink

class FoodAndDrinkForm(forms.ModelForm):
    class Meta:
        model = FoodAndDrink
        fields = '__all__'
