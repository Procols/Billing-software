# reports/forms.py
from django import forms

class ReportFilterForm(forms.Form):
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    payment_status = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Select Payment Status'),
            ('paid', 'Paid'),
            ('cancelled', 'Cancelled'),
            ('pending', 'Pending'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
