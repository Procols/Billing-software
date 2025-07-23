from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required(login_url='accounts:login')
def dashboard_view(request):
    if request.user.is_admin():
        # Optional: redirect admin to their own panel
        return redirect('admin:index')  # or to your future custom admin page
    elif request.user.is_receptionist():
        return render(request, 'core/dashboard.html')  # ✅ receptionist view

    return redirect('accounts:login')  # fallback

