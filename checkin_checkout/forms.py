from django import forms
from .models import CheckIn
from rooms.models import Room

class CheckInForm(forms.ModelForm):
    class Meta:
        model = CheckIn
        fields = ['guest_name', 'phone', 'room', 'check_in', 'check_out', 'members']

        widgets = {
            'check_in': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'check_out': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_out and check_in and check_out < check_in:
            raise forms.ValidationError("Check-out date/time cannot be before check-in date/time.")
