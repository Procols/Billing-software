from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User  # ✅ This is the missing import

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'is_active', 'is_staff')
