from django import forms
from .models import FoodAndDrink
from rooms.models import Room
from booking.models import Booking

class FoodAndDrinkForm(forms.ModelForm):
    class Meta:
        model = FoodAndDrink
        fields = ['booking','room','phone_number','food_item','food_price','drink_item','drink_price']
        widgets = {
            'food_price': forms.NumberInput(attrs={'step':'0.01'}),
            'drink_price': forms.NumberInput(attrs={'step':'0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['booking'].required = False
        self.fields['booking'].queryset = Booking.objects.all().order_by('-created_at')
        self.fields['room'].queryset = Room.objects.all().order_by('room_number')
