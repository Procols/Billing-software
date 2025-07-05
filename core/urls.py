from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('login')),  
    path('home/', views.index, name='home')
    
]
