from django.shortcuts import render, redirect
from .forms import FoodAndDrinkForm
from .models import FoodAndDrink
from rooms.models import Room


def food_drink_entry(request):
    if request.method == 'POST':
        form = FoodAndDrinkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('foods:food_entry')
    else:
        form = FoodAndDrinkForm()

    form.fields['room'].queryset = Room.objects.filter(status='Occupied')

    return render(request, 'food_drinks/entry.html', {'form': form})