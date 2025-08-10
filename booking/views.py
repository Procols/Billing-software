from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Booking
from .forms import BookingForm
from rooms.models import Room
from checkin_checkout.models import CheckIn
from django.utils.timezone import localdate

def booking_list(request):
    bookings = Booking.objects.select_related('room').order_by('-created_at')
    return render(request, 'booking/booking_list.html', {'bookings': bookings})

def new_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            # create or update CheckIn record
            CheckIn.objects.update_or_create(booking=booking, defaults={'status': 'active'})
            return redirect('booking:booking_list')
    else:
        form = BookingForm()
    # pass list of available rooms for convenience (template uses it)
    rooms = Room.objects.filter(status='Available').order_by('room_number')
    return render(request, 'booking/new_booking.html', {'form': form, 'rooms': rooms})

def get_room_details(request):
    room_id = request.GET.get('room_id')
    try:
        room = Room.objects.get(id=room_id)
        data = {
            'room_type': room.room_type,
            'ac_type': room.ac_type,
            'floor': str(room.floor) if room.floor else '',
            'status': room.status,
            'price': float(room.price),
        }
        return JsonResponse(data)
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)

def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    # foods for this booking (foods app must exist)
    from foods.models import FoodAndDrink
    foods = FoodAndDrink.objects.filter(booking=booking).order_by('-created_at')

    # print action: set checkout_date to today if not set, mark completed, update checkin
    if request.method == 'POST' and request.POST.get('action') == 'print':
        if not booking.checkout_date:
            booking.checkout_date = localdate()
            booking.save()
            # update checkin
            ci = CheckIn.objects.filter(booking=booking).first()
            if ci:
                ci.status = 'checked_out'
                ci.save()
        # redirect to same url with ?print=1 so JS triggers window.print()
        return redirect(request.path + '?print=1')

    return render(request, 'booking/booking_detail.html', {'booking': booking, 'foods': foods})
