from django import forms
from .models import RoomType, Room

class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ['name', 'base_rate', 'description', 'amenities', 'floor']
        labels = {
            'name': 'Enter Room Type Name',
            'base_rate': 'Enter Base Rate',
            'description': 'Enter Description',
            'amenities': 'Enter Amenities',
            'floor': 'Select Floor',
        }
        widgets = {
            'floor': forms.Select()
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'floor', 'rate_per_night', 'status']
        labels = {
            'room_number': 'Enter Room Number',
            'room_type': 'Select Room Type',
            'floor': 'Select Floor',
            'rate_per_night': 'Enter Rate Per Night',
            'status': 'Select Status',
        }
        widgets = {
            'floor': forms.Select(),
            'room_type': forms.Select(),
            'status': forms.Select()
        }
