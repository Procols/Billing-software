from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('', views.payment_list, name='payment_list'),
]
