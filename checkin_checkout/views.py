from django.shortcuts import render
from booking.models import Booking
from django.utils.timezone import now

def checkin_checkout_view(request):
    # Fetch bookings that are currently active (status booked)
    active_bookings = Booking.objects.filter(status='booked')

    # Optionally, update bookings where checkout_date passed
    for booking in active_bookings:
        if booking.checkout_date and booking.checkout_date <= now():
            booking.status = 'completed'
            booking.save()

            # Update room status to Available
            room = booking.room
            room.status = 'Available'
            room.save()

    context = {
        'active_bookings': Booking.objects.filter(status='booked'),
        'completed_bookings': Booking.objects.filter(status='completed'),
    }
    return render(request, 'checkin/checkin_checkout.html', context)
