from django import forms
from .models import RoomType, Room

class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ['name', 'ac_type', 'description', 'amenities']
        labels = {
            'name': 'Enter Room Type Name',
            'ac_type': 'Select AC Type',
            'description': 'Enter Description',
            'amenities': 'Enter Amenities',
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