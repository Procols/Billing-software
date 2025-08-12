from django.contrib import admin
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'invoice_number', 'customer_name', 'status', 'room',
        'checkin_datetime', 'checkout_datetime',  # updated field names here
        'price', 'created_at'
    ]
    # add other config if any

admin.site.register(Booking, BookingAdmin)
