from django.urls import path
from . import views

app_name = 'checkin_checkout'

urlpatterns = [
    path('', views.checkin_checkout_view, name='checkin_checkout'),
]
