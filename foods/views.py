from django.shortcuts import render, redirect
from .forms import FoodAndDrinkForm
from .models import FoodAndDrink

def food_drink_entry(request):
    if request.method == 'POST':
        form = FoodAndDrinkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('foods:food_entry')
    else:
        form = FoodAndDrinkForm()
    return render(request, 'foods/food_drink_entry.html', {'form': form})
