from django.contrib import admin
from .models import Floor, Room

@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('number',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'get_room_type_display', 'get_ac_type_display', 'floor', 'price', 'status')
    list_filter = ('room_type', 'ac_type', 'status', 'floor')
    search_fields = ('room_number',)
