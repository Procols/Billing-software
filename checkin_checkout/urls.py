# checkin_checkout/urls.py
from django.urls import path
from . import views

app_name = 'checkin_checkout' 

urlpatterns = [
    path('', views.checkin_checkout_view, name='checkin_checkout'),
    path('update_checkout/<int:booking_id>/', views.update_checkout, name='update_checkout'),
    path('view/<int:booking_id>/', views.booking_view_details, name='view_details'),
    path('invoice/<int:booking_id>/', views.invoice_view, name='invoice'),
]
