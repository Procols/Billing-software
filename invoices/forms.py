from django import forms

STATUS_CHOICES = [
    ('paid', 'Paid'),
    ('pending', 'Pending'),
]

class InvoiceFilterForm(forms.Form):
    invoice_number = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Search by Invoice No.',
        'class': 'form-control',
        'style': 'width: 180px;'
    }))
    guest_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Search by Guest Name',
        'class': 'form-control',
        'style': 'width: 180px;'
    }))
    status = forms.ChoiceField(required=False, choices=[('', 'All Statuses')] + STATUS_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select',
        'style': 'width: 150px;'
    }))
