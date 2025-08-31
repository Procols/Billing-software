from django import forms

class TaxFilterForm(forms.Form):
    invoice = forms.CharField(required=False, label="Invoice Number")
    from_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    min_gst = forms.DecimalField(required=False, min_value=0, label="Min GST ₹")
    max_gst = forms.DecimalField(required=False, min_value=0, label="Max GST ₹")
