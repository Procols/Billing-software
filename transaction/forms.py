from django import forms

# Choices for filtering payment type
PAYMENT_CHOICES = [
    ('All', 'All Payment Modes'),
    ('cash', 'Cash'),
    ('upi', 'UPI'),
    ('card', 'Card'),
]

class PaymentFilterForm(forms.Form):
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        ),
        label='Start Date'
    )
    payment_mode = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Payment Mode'
    )
