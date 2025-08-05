from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'customer_name', 'phone_number', 'address', 'document_type', 'document_number',
            'room', 'adults', 'children', 'booking_status', 'checkin_date', 'checkout_date',
            'payment_type', 'apply_gst'
        ]
