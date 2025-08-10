from django.db import models
from django.utils.timezone import localdate
from rooms.models import Room

class Booking(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
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
    document_type = models.CharField(max_length=50, choices=[('Aadhar','Aadhar'), ('License','License'), ('PAN','PAN')], default='Aadhar')
    document_number = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')
    checkin_date = models.DateField(default=localdate)    # DATE only
    checkout_date = models.DateField(blank=True, null=True)  # optional, DATE only

    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cash')
    apply_gst = models.BooleanField(default=False)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # invoice generation
        if not self.invoice_number:
            last = Booking.objects.order_by('-id').first()
            if last and last.invoice_number and last.invoice_number.startswith("INV-"):
                try:
                    last_num = int(last.invoice_number.replace("INV-", ""))
                    new_num = last_num + 1
                except:
                    new_num = 1001
            else:
                new_num = 1001
            self.invoice_number = f"INV-{new_num}"

        # price calculation based on room price and GST
        base = self.room.price
        if self.apply_gst:
            self.price = base + (base * 0.18)
        else:
            self.price = base

        # auto-complete if checkout_date present and <= today
        if self.checkout_date:
            if self.checkout_date <= localdate():
                self.status = 'completed'

        super().save(*args, **kwargs)

        # update room status depending on booking status
        if self.status == 'booked':
            if self.room.status != 'Occupied':
                self.room.status = 'Occupied'
                self.room.save()
        elif self.status == 'completed':
            if self.room.status != 'Available':
                self.room.status = 'Available'
                self.room.save()

    def __str__(self):
        return f"{self.invoice_number} - {self.customer_name}"
