# foods/admin.py
from django.contrib import admin
from .models import FoodAndDrink
from rooms.models import Room

class FoodAndDrinkAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "room":
            kwargs["queryset"] = Room.objects.filter(status="Occupied")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(FoodAndDrink, FoodAndDrinkAdmin)
