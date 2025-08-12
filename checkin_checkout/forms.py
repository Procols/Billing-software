from django import forms
from booking.models import Booking

class BookingUpdateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'customer_name', 'phone_number', 'address', 'document_type', 'document_number',
            'adults', 'children', 'status', 'checkin_datetime', 'checkout_datetime',
            'payment_type', 'apply_gst'
        ]
        widgets = {
            'checkin_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'checkout_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class UpdateCheckoutForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['checkout_datetime', 'status']
        widgets = {
            'checkout_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'status': forms.Select()
        }

    def clean(self):
        cleaned_data = super().clean()
        checkout = cleaned_data.get('checkout_datetime')
        checkin = self.instance.checkin_datetime

        if checkout and checkin and checkout < checkin:
            raise forms.ValidationError("Checkout cannot be before check-in.")
