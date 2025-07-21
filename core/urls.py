from django.urls import path
from django.shortcuts import redirect
from .views import dashboard_view

app_name = 'core'

urlpatterns = [
    path('', lambda request: redirect('accounts:login') if not request.user.is_authenticated else redirect('core:dashboard'), name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
