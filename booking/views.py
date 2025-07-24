from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Booking
from .forms import BookingForm

def bookings_overview(request):
    bookings = Booking.objects.all().order_by('-created_at')
    total_bookings = bookings.count()
    pending_payments = bookings.filter(payment_status='pending').aggregate(total=Sum('room_price'))['total'] or 0
    available_rooms = 25  # You can update this logic later based on your room availability model

    context = {
        'bookings': bookings,
        'total_bookings': total_bookings,
        'pending_payments': pending_payments,
        'available_rooms': available_rooms,
    }
    return render(request, 'bookings/bookings.html', context)

def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking:overview')
    else:
        form = BookingForm()

    return render(request, 'bookings/booking_form.html', {'form': form})

def booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking:overview')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'bookings/booking_form.html', {'form': form})

def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        return redirect('booking:overview')
    return render(request, 'bookings/booking_confirm_delete.html', {'booking': booking})
