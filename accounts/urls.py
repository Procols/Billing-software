from django.urls import path
from .views import login_view, logout_view, create_receptionist_view

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create-receptionist/', create_receptionist_view, name='create-receptionist'),
]
