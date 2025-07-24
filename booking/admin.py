from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'customer_name', 'room', 'check_in_date', 'check_out_date', 'status', 'payment_status')
    list_filter = ('status', 'payment_status', 'payment_method', 'floor')
    search_fields = ('booking_id', 'customer_name', 'phone_number', 'room')
