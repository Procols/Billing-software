from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'customer_name', 'room', 'booking_status', 'checkin_date', 'checkout_date', 'price')
    list_filter = ('booking_status', 'payment_type', 'apply_gst')
    search_fields = ('invoice_number', 'customer_name', 'room__room_number')
