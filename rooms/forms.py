from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'ac_type', 'floor', 'price', 'status']
        labels = {
            'room_number': 'Enter Room Number',
            'room_type': 'Select Room Type',
            'ac_type': 'Select AC Type',
            'floor': 'Select Floor',
            'price': 'Enter Room Price',
            'status': 'Select Status',
        }

class RoomUpdateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_type', 'ac_type', 'floor', 'price', 'status']
        labels = {
            'room_type': 'Select Room Type',
            'ac_type': 'Select AC Type',
            'floor': 'Select Floor',
            'price': 'Enter Room Price',
            'status': 'Select Status',
        }
