from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required(login_url='accounts:login')
def dashboard_view(request):
    if request.user.role != 'admin':
        return redirect('accounts:login')
    return render(request, 'core/dashboard.html')
