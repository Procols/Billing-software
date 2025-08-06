from django.contrib import admin
from .models import FoodAndDrink

@admin.register(FoodAndDrink)
class FoodAndDrinkAdmin(admin.ModelAdmin):
    list_display = ('room', 'phone_number', 'food_item', 'food_price', 'drink_item', 'drink_price', 'created_at')
    search_fields = ('room__room_number', 'phone_number', 'food_item', 'drink_item')