from django.shortcuts import render, redirect
from rooms.models import Room
from booking.models import Booking
from .models import FoodAndDrink

def food_drink_entry(request):
    occupied_rooms = Room.objects.filter(status='Occupied')
    bookings = Booking.objects.filter(room__in=occupied_rooms, status__in=['booked', 'pre_booked'])

    if request.method == 'POST':
        room_id = request.POST.get('room')
        phone_number = request.POST.get('phone_number')

        food_items = request.POST.getlist('food_item')
        food_prices = request.POST.getlist('food_price')
        drink_items = request.POST.getlist('drink_item')
        drink_prices = request.POST.getlist('drink_price')

        try:
            room = Room.objects.get(id=room_id)
            booking = Booking.objects.filter(room=room, status__in=['booked', 'pre_booked']).first()
        except Room.DoesNotExist:
            room = None
            booking = None

        if room and booking:
            for f_item, f_price, d_item, d_price in zip(food_items, food_prices, drink_items, drink_prices):
                if f_item.strip() or d_item.strip():
                    FoodAndDrink.objects.create(
                        booking=booking,
                        room=room,
                        phone_number=phone_number or '',
                        food_item=f_item or '',
                        food_price=f_price if f_price else 0,
                        drink_item=d_item or '',
                        drink_price=d_price if d_price else 0,
                    )
            return redirect('foods:food_entry')

    # Show all food orders
    food_orders = FoodAndDrink.objects.select_related('room', 'booking').order_by('-created_at')

    return render(request, 'food_drinks/food_drink_entry.html', {
        'bookings': bookings,
        'food_orders': food_orders,
    })
