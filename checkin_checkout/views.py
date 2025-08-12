from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import localdate
from booking.models import Booking
from rooms.models import Room
from foods.models import FoodAndDrink
from .models import CheckIn
from .forms import UpdateCheckoutForm, BookingUpdateForm

def checkin_checkout_view(request):
    today = localdate()

    # Auto-update bookings if checkout date passed
    for b in Booking.objects.filter(status='booked'):
        if b.checkout_datetime and b.checkout_datetime.date() <= today:
            b.status = 'completed'
            b.save()
            if b.room:
                b.room.status = 'available'
                b.room.save()
            ci, _ = CheckIn.objects.get_or_create(booking=b)
            ci.status = 'checked_out'
            ci.save()

    bookings = Booking.objects.all().order_by('-created_at')

    context = {'bookings': bookings}
    return render(request, 'checkin/checkin_checkout.html', context)


def update_checkout(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        form = UpdateCheckoutForm(request.POST, instance=booking)
        if form.is_valid():
            updated_booking = form.save()

            # Update room and checkin status accordingly
            if updated_booking.status == 'completed' and updated_booking.room:
                updated_booking.room.status = 'available'
                updated_booking.room.save()
                ci, _ = CheckIn.objects.get_or_create(booking=updated_booking)
                ci.status = 'checked_out'
                ci.save()
            elif updated_booking.status == 'booked' and updated_booking.room:
                updated_booking.room.status = 'occupied'
                updated_booking.room.save()
                ci, _ = CheckIn.objects.get_or_create(booking=updated_booking)
                ci.status = 'active'
                ci.save()

            return redirect('checkin:checkin_checkout')
        else:
            # print errors for debugging
            print(form.errors)
    else:
        form = UpdateCheckoutForm(instance=booking)

    return render(request, 'checkin/update_checkout.html', {'form': form, 'booking': booking})


def booking_view_details(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    food_orders = FoodAndDrink.objects.filter(booking=booking)

    if request.method == 'POST':
        form = BookingUpdateForm(request.POST, instance=booking)
        if form.is_valid():
            updated_booking = form.save()
            # Update room status
            if updated_booking.status == 'completed' and updated_booking.room:
                updated_booking.room.status = 'available'
                updated_booking.room.save()
            elif updated_booking.status == 'booked' and updated_booking.room:
                updated_booking.room.status = 'occupied'
                updated_booking.room.save()

            return redirect('checkin:view_details', booking_id=booking.id)
    else:
        form = BookingUpdateForm(instance=booking)

    # Calculate total days
    total_days = 0
    if booking.checkin_datetime and booking.checkout_datetime:
        total_days = (booking.checkout_datetime.date() - booking.checkin_datetime.date()).days
        if total_days < 0:
            total_days = 0

    # Room price and food total for invoice
    room_price = getattr(booking.room, 'price', 0) or 0
    room_amount = room_price * total_days

    # Add subtotal attribute to each food order item
    for item in food_orders:
        qty = getattr(item, 'quantity', 1) or 1
        item.subtotal = item.price * qty

    food_amount = sum(item.subtotal for item in food_orders)

    amount_paid = getattr(booking, 'amount_paid', 0) or 0
    balance_due = room_amount + food_amount - amount_paid

    context = {
        'booking': booking,
        'form': form,
        'food_orders': food_orders,
        'total_days': total_days,
        'room_price': room_price,
        'room_amount': room_amount,
        'food_amount': food_amount,
        'amount_paid': amount_paid,
        'balance_due': balance_due,
    }
    return render(request, 'checkin/view_details.html', context)



def invoice_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    total_days = 0
    if booking.checkin_datetime and booking.checkout_datetime:
        total_days = (booking.checkout_datetime.date() - booking.checkin_datetime.date()).days
        if total_days < 0:
            total_days = 0

    food_orders = FoodAndDrink.objects.filter(booking=booking)

    room_price = getattr(booking.room, 'price', 0) or 0
    room_amount = room_price * total_days

    # Calculate subtotal for each food item and add as attribute
    for item in food_orders:
        qty = getattr(item, 'quantity', 1) or 1
        item.subtotal = item.price * qty

    food_amount = sum(item.subtotal for item in food_orders)

    amount_paid = getattr(booking, 'amount_paid', 0) or 0
    balance_due = room_amount + food_amount - amount_paid

    context = {
        'booking': booking,
        'food_orders': food_orders,
        'total_days': total_days,
        'room_price': room_price,
        'room_amount': room_amount,
        'food_amount': food_amount,
        'amount_paid': amount_paid,
        'balance_due': balance_due,
    }
    return render(request, 'checkin/invoice.html', context)
