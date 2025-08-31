from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username', 'id': 'id_username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'id': 'id_password'})
    )


class ReceptionistCreateForm(forms.ModelForm):
    """
    Only Admin/Sub Admin can use this, and it always creates a Receptionist.
    """
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Set password', 'autocomplete': 'new-password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'autocomplete': 'new-password'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email (optional)'}),
        }

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('confirm_password')
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        # Force role & flags
        user.role = User.ROLE_RECEPTIONIST
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user
