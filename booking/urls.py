from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.bookings_overview, name='overview'),
    path('new/', views.booking_create, name='new'),
]
