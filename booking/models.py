from django.db import models
from rooms.models import Room 
from django.utils.timezone import now

class Booking(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('prebooked', 'Pre-Booked'),
    ]

    PAYMENT_CHOICES = [
        ('upi', 'UPI'),
        ('cash', 'Cash'),
        ('card', 'Card'),
    ]

    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    document_type = models.CharField(
        max_length=50,
        choices=[('Aadhar', 'Aadhar Number'), ('License', "Driver's License"), ('PAN', 'PAN Number')],
        default='Aadhar'
    )
    document_number = models.CharField(max_length=50)

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)

    booking_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')
    
    checkin_date = models.DateField(default=now)
    checkout_date = models.DateField(default=now)

    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cash')
    apply_gst = models.BooleanField(default=False)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    invoice_number = models.CharField(max_length=20, unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            last_booking = Booking.objects.order_by('-id').first()
            if last_booking and last_booking.invoice_number and last_booking.invoice_number.startswith("INV-"):
                last_number = int(last_booking.invoice_number.replace("INV-", ""))
                new_number = last_number + 1
            else:
                new_number = 1001
            self.invoice_number = f"INV-{new_number}"

        base_price = self.room.price
        if self.apply_gst:
            self.price = base_price + (base_price * 0.18)
        else:
            self.price = base_price

        super().save(*args, **kwargs)
