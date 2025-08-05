from django.urls import path
from . import views
from django.views.generic import RedirectView

app_name = "booking"

urlpatterns = [
    path("list/", views.booking_list, name="booking_list"),
    path("new/", views.new_booking, name="new_booking"),
    path("get-room-details/", views.get_room_details, name="get_room_details"),
    # Redirect '/booking/' to '/booking/list/'
    path('', RedirectView.as_view(pattern_name='booking:booking_list', permanent=False)),
]
