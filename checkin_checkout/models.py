from django.db import models
from booking.models import Booking

class CheckIn(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('checked_out', 'Checked Out')
    ], default='active')

    def __str__(self):
        return f"{self.booking.guest_name} - {self.status}"
