from django.contrib import admin
from .models import Room, Floor

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'ac_type', 'floor', 'price', 'status')
    list_filter = ('room_type', 'ac_type', 'status', 'floor')
    search_fields = ('room_number',)


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('number',)
