from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'customer_name', 'phone_number', 'address', 'document_type', 'document_number',
            'room', 'adults', 'children', 'status', 'checkin_date', 'checkout_date',
            'payment_type', 'apply_gst'
        ]
        widgets = {
            'checkin_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'checkout_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['checkout_date'].required = False  # make checkout optional

        # Limit room choices to available rooms only
        self.fields['room'].queryset = self.fields['room'].queryset.filter(status='Available')
