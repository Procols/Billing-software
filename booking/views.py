from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import BookingForm
from .models import Booking
from rooms.models import Room

def new_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking:booking_list')
    else:
        form = BookingForm()

    # No need to pass rooms separately — form limits available rooms already
    return render(request, 'booking/new_booking.html', {'form': form})

def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'booking/booking_list.html', {'bookings': bookings})

def get_room_details(request):
    room_id = request.GET.get('room_id')
    try:
        room = Room.objects.get(id=room_id)
        data = {
            'room_type': room.room_type,
            'ac_type': room.ac_type,
            'floor': str(room.floor),
            'status': room.status,
            'price': float(room.price),
        }
        return JsonResponse(data)
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)
