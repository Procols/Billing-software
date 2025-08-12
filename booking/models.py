from django.db import models
from django.utils.timezone import now
from rooms.models import Room

class Booking(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('pre_booked', 'Pre Booked'),
        ('completed', 'Completed'),
    ]

    PAYMENT_CHOICES = [
        ('upi', 'UPI'),
        ('cash', 'Cash'),
        ('card', 'Card'),
    ]

    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    document_type = models.CharField(max_length=50, choices=[('Aadhar', 'Aadhar'), ('License', 'License'), ('PAN', 'PAN')], default='Aadhar')
    document_number = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pre_booked')
    checkin_datetime = models.DateTimeField(default=now)  # mandatory now
    checkout_datetime = models.DateTimeField(blank=True, null=True)  # optional

    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cash')
    apply_gst = models.BooleanField(default=False)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        # Calculate price with GST if applicable before saving
        base_price = self.room.price
        self.price = base_price + (base_price * 0.18) if self.apply_gst else base_price

        # Auto update status to completed if checkout_datetime <= now()
        if self.checkout_datetime and self.checkout_datetime <= now():
            self.status = 'completed'

        super().save(*args, **kwargs)  # Save first to get pk

        # Generate invoice_number only once on creation
        if is_new and not self.invoice_number:
            self.invoice_number = f"INV-{100 + self.id}"
            Booking.objects.filter(pk=self.pk).update(invoice_number=self.invoice_number)

        # Update room status based on booking status
        if self.status in ('booked', 'pre_booked'):
            if self.room.status != 'Occupied':
                self.room.status = 'Occupied'
                self.room.save()
        elif self.status == 'completed':
            if self.room.status != 'Available':
                self.room.status = 'Available'
                self.room.save()

    def __str__(self):
        return f"{self.invoice_number} - {self.customer_name}"
