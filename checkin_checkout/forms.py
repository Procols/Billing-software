from django import forms
from booking.models import Booking


class BookingUpdateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'customer_name', 'phone_number', 'address', 'document_type', 'document_number',
            'adults', 'children', 'status', 'checkin_datetime', 'checkout_datetime',
            'payment_type', 'payment_status', 'apply_gst', 'amount_paid'
        ]
        widgets = {
            'checkin_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'readonly': 'readonly'}),
            'checkout_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'readonly': 'readonly'}),
            'customer_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'phone_number': forms.TextInput(attrs={'readonly': 'readonly'}),
            'address': forms.Textarea(attrs={'readonly': 'readonly', 'rows': 2}),
            'document_type': forms.TextInput(attrs={'readonly': 'readonly'}),
            'document_number': forms.TextInput(attrs={'readonly': 'readonly'}),
            'adults': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'children': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'status': forms.Select(attrs={'readonly': True}),
            'apply_gst': forms.CheckboxInput(attrs={'disabled': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only allow editing of payment_type, payment_status, and amount_paid
        for field in self.fields:
            if field not in ['payment_type', 'payment_status', 'amount_paid']:
                self.fields[field].disabled = True


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
        return cleaned_data
