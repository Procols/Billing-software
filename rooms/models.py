from django.db import models

def get_default_floor():
    # Always reference an existing floor ID (default: 1)
    return Floor.objects.get_or_create(number=1)[0].id

class Floor(models.Model):
    number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        # Format ordinal suffix
        if 10 <= self.number % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(self.number % 10, "th")
        return f"{self.number}{suffix} Floor"

class RoomType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    amenities = models.TextField(null=False, blank=True)

    base_rate = models.DecimalField(max_digits=8, decimal_places=2)
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, null=True, default=get_default_floor)

    def __str__(self):
        return self.name

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
