from django.db import models

def get_default_floor():
    return Floor.objects.get_or_create(number=1)[0].id

class Floor(models.Model):
    number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        if 10 <= self.number % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(self.number % 10, "th")
        return f"{self.number}{suffix} Floor"

class RoomType(models.Model):
    AC_CHOICES = [
        ('ac', 'A/C'),
        ('non-ac', 'Non A/C'),
    ]
    name = models.CharField(max_length=100, unique=True)
    ac_type = models.CharField(max_length=10, choices=AC_CHOICES, default='non-ac')
    description = models.TextField(blank=True)
    amenities = models.TextField(blank=True)
    

    def __str__(self):
        return self.name

    def is_ac(self):
        return self.ac_type == 'ac'

class Room(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
    ]
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, null=True, default=get_default_floor)
    rate_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type.name})"