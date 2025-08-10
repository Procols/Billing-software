from django.db import models
from rooms.models import Room
from booking.models import Booking

class FoodAndDrink(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    food_item = models.CharField(max_length=100, blank=True, null=True)
    food_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    drink_item = models.CharField(max_length=100, blank=True, null=True)
    drink_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order for Room {self.room.room_number}"
