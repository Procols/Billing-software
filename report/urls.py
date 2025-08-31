# report/urls.py
from django.urls import path
from . import views

app_name = 'report'

urlpatterns = [
    path('', views.booking_report, name='booking_report'),
]
