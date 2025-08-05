from django.db import models

def get_default_floor():
    return Floor.objects.get_or_create(number=1)[0].id

class Floor(models.Model):
    number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        suffix = "th"
        if 10 <= self.number % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(self.number % 10, "th")
        return f"{self.number}{suffix} Floor"


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
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, null=True, default=get_default_floor)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type} - {self.ac_type})"
