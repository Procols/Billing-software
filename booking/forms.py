from django import forms
from .models import Booking
from rooms.models import Room

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'customer_name', 'phone_number', 'address', 'document_type', 'document_number',
            'room', 'adults', 'children', 'status', 'checkin_date', 'checkout_date',
            'payment_type', 'apply_gst'
        ]
        widgets = {
            'checkin_date': forms.DateInput(attrs={'type':'date'}),
            'checkout_date': forms.DateInput(attrs={'type':'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # only available rooms for booking
        self.fields['room'].queryset = Room.objects.filter(status='Available').order_by('room_number')
        self.fields['checkout_date'].required = False
