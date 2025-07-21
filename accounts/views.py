from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm, AssistantCreateForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log user in, set session
            if user.role == 'admin':
                return redirect('core:dashboard')
            else:
                # You can create receptionist dashboard or change this redirect
                return redirect('accounts:login')
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
