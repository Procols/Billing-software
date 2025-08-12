from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.booking_list, name='booking_list'),
    path('new/', views.new_booking, name='new_booking'),
    path('get-room-details/', views.get_room_details, name='get_room_details'),
    path('<str:pk>/', views.booking_detail, name='booking_detail'),  # pk is invoice_number now string
]
