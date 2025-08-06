from django import forms
from .models import FoodAndDrink


class FoodAndDrinkForm(forms.ModelForm):
    class Meta:
        model = FoodAndDrink
        fields = ['room', 'phone_number', 'food_item', 'food_price', 'drink_item', 'drink_price']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
            'food_item': forms.TextInput(attrs={'placeholder': 'Enter food item'}),
            'food_price': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00'}),
            'drink_item': forms.TextInput(attrs={'placeholder': 'Enter drink item'}),
            'drink_price': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['food_item'].required = False
        self.fields['food_price'].required = False
        self.fields['drink_item'].required = False
        self.fields['drink_price'].required = False
