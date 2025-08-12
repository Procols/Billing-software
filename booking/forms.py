from django import forms
from .models import Booking
from rooms.models import Room

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'customer_name', 'phone_number', 'address', 'document_type', 'document_number',
            'room', 'adults', 'children', 'status', 'checkin_datetime', 'checkout_datetime',
            'payment_type', 'apply_gst'
        ]
        widgets = {
            'checkin_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'checkout_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make checkin_datetime required
        self.fields['checkin_datetime'].required = True
        self.fields['checkout_datetime'].required = False

        # Show only rooms with status Available
        self.fields['room'].queryset = Room.objects.filter(status='Available').order_by('room_number')
