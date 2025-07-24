from django.db import models

class Booking(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
    ]

    DOCUMENT_TYPES = [
        ('aadhar', 'Aadhar'),
        ('passport', 'Passport'),
        ('voter_id', 'Voter ID'),
        ('driver_license', 'Driver License'),
        # add more if needed
    ]

    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
        ('checkedout', 'Checked Out'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
    ]

    booking_id = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField(blank=True)

    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_number = models.CharField(max_length=50)

    check_in_date = models.DateField()
    check_in_time = models.TimeField()
    check_out_date = models.DateField()
    check_out_time = models.TimeField()

    floor = models.PositiveIntegerField()  # or ForeignKey to Floor if you want
    room = models.CharField(max_length=10)  # room number as string for simplicity

    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)

    room_service = models.BooleanField(default=False)
    food_included = models.BooleanField(default=False)

    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    room_price = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking_id} - {self.customer_name}"
