from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm, AssistantCreateForm
from django.urls import reverse

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log the user in

            # 🚀 Role-based redirect
            if user.is_admin():
                return redirect(reverse('core:dashboard'))  # Django admin panel
            elif user.is_receptionist():
                return redirect('core:dashboard')  # receptionist dashboard

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def create_assistant_view(request):
    if request.method == 'POST':
        form = AssistantCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = AssistantCreateForm()
    return render(request, 'accounts/create_assistant.html', {'form': form})
