from django.shortcuts import render
from booking.models import Booking
from django.utils.timezone import localdate
from .models import CheckIn

def checkin_checkout_view(request):
    # auto-update bookings with past checkout_date
    today = localdate()
    updated = []
    for b in Booking.objects.filter(status='booked'):
        if b.checkout_date and b.checkout_date <= today:
            b.status = 'completed'
            b.save()
            ci, _ = CheckIn.objects.get_or_create(booking=b)
            ci.status = 'checked_out'
            ci.save()
            updated.append(b.id)

    context = {
        'active_bookings': Booking.objects.filter(status='booked').order_by('-created_at'),
        'completed_bookings': Booking.objects.filter(status='completed').order_by('-created_at'),
    }
    return render(request, 'checkin/checkin_checkout.html', context)
