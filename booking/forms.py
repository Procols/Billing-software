from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'customer_name', 'phone_number', 'address',
            'document_type', 'document_number',
            'check_in_date', 'check_in_time', 'check_out_date', 'check_out_time',
            'floor', 'room',
            'adults', 'children',
            'room_service', 'food_included',
            'payment_method', 'room_price',
            'status', 'payment_status',
        ]
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_in_time': forms.TimeInput(attrs={'type': 'time'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_time': forms.TimeInput(attrs={'type': 'time'}),
        }
