# setting/forms.py
from django import forms
from django.contrib.auth import get_user_model
from .models import SiteConfig

User = get_user_model()

class SiteConfigForm(forms.ModelForm):
    class Meta:
        model = SiteConfig
        fields = ['site_name', 'support_email', 'support_phone']
        widgets = {
            'site_name': forms.TextInput(attrs={'class':'form-control'}),
            'support_email': forms.EmailInput(attrs={'class':'form-control'}),
            'support_phone': forms.TextInput(attrs={'class':'form-control'}),
        }

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        # edit basic fields + role
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'role': forms.Select(attrs={'class':'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }
