from django.urls import path
from . import views

app_name = 'foods'

urlpatterns = [
    path('', views.food_drink_entry, name='food_entry'),
]