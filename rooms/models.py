from django.db import models

def get_default_floor():
    # create floor 1 if not exists and return object (used for FK default)
    floor, _ = Floor.objects.get_or_create(number=1)
    return floor

class Floor(models.Model):
    number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        n = self.number
        if 10 <= n % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return f"{n}{suffix} Floor"

class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('Standard', 'Standard'),
        ('Deluxe', 'Deluxe'),
        ('Suite', 'Suite'),
    ]

    AC_CHOICES = [
        ('AC', 'A/C'),
        ('Non-AC', 'Non A/C'),
    ]

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Occupied', 'Occupied'),
        ('Maintenance', 'Maintenance'),
    ]

    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    ac_type = models.CharField(max_length=10, choices=AC_CHOICES, default='Non-AC')
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, null=True, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type} - {self.ac_type})"
