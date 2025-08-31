from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm, ReceptionistCreateForm  # Corrected import
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .decorators import admins_only


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log the user in

            # 🚀 Redirect all users to dashboard
            return redirect(reverse('core:dashboard'))
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@admins_only
def create_receptionist_view(request):
    """
    Only Admin/Sub Admin can create Receptionist
    """
    if request.method == 'POST':
        form = ReceptionistCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = ReceptionistCreateForm()
    
    return render(request, 'accounts/create_receptionist.html', {'form': form})
