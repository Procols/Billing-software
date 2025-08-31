from django.db import models
from django.utils.timezone import now
from rooms.models import Room
from decimal import Decimal


class Booking(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('pre-booked', 'Pre-Booked'),
        ('completed', 'Completed'),
    ]

    PAYMENT_CHOICES = [
        ('upi', 'UPI'),
        ('cash', 'Cash'),
        ('card', 'Card'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
    ]

    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    document_type = models.CharField(
        max_length=50,
        choices=[('Aadhar', 'Aadhar'), ('License', 'License'), ('PAN', 'PAN')],
        default='Aadhar'
    )
    document_number = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')
    checkin_datetime = models.DateTimeField(default=now)
    checkout_datetime = models.DateTimeField(blank=True, null=True)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cash')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    apply_gst = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # final total price
    cgst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sgst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    invoice_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_persons(self):
        return self.adults + self.children

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        # Calculate stay duration
        total_days = 1
        if self.checkin_datetime and self.checkout_datetime:
            total_days = max(1, (self.checkout_datetime.date() - self.checkin_datetime.date()).days)

        base_price = Decimal(getattr(self.room, 'price', 0) or 0)
        total_room_price = base_price * Decimal(total_days)

        # GST Calculation (split CGST + SGST equally)
        if self.apply_gst:
            gst_rate = Decimal('0.12') if total_room_price < Decimal('7000.00') else Decimal('0.18')
            gst_amount = total_room_price * gst_rate
            self.cgst_amount = gst_amount / 2
            self.sgst_amount = gst_amount / 2
            self.price = total_room_price + gst_amount
        else:
            self.cgst_amount = Decimal(0)
            self.sgst_amount = Decimal(0)
            self.price = total_room_price

        # Auto-complete booking if checkout passed
        from django.utils.timezone import now as timezone_now
        if self.checkout_datetime and self.checkout_datetime <= timezone_now():
            self.status = 'completed'

        # Generate invoice number
        if not self.invoice_number and is_new:
            last_booking = Booking.objects.order_by('-id').first()
            last_id = last_booking.id if last_booking else 0
            self.invoice_number = f"INV-{100 + last_id + 1}"

        super().save(*args, **kwargs)

        # Update room status
        if self.status in ('booked', 'pre-booked'):
            self.room.status = 'Occupied'
        elif self.status == 'completed' or self.payment_status == 'cancelled':
            self.room.status = 'Available'
        self.room.save()
