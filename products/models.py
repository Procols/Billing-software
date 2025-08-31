from django.db import models
from django.utils import timezone


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('cleaning', 'Cleaning'),
        ('kitchen', 'Kitchen'),
        ('maintenance', 'Room Maintenance'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="other")
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def total_value(self):
        return self.quantity * self.unit_price

    def is_low_stock(self):
        return self.quantity <= 5
