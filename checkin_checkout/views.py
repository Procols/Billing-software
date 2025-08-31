from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import localdate, now
from booking.models import Booking
from rooms.models import Room
from foods.models import FoodAndDrink
from .models import CheckIn
from .forms import UpdateCheckoutForm, BookingUpdateForm
from decimal import Decimal
from collections import defaultdict

# ----------------- Checkin/Checkout Dashboard -----------------
def checkin_checkout_view(request):
    today = localdate()

    # Auto mark completed if checkout <= today
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

    bookings = Booking.objects.all().select_related("room").order_by("-created_at")

    # Search filters
    query = request.GET.get("q", "").strip()
    checkin_from = request.GET.get("checkin_from")
    checkin_to = request.GET.get("checkin_to")

    if query:
        bookings = bookings.filter(
            Q(customer_name__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(room__room_number__icontains=query) |
            Q(status__icontains=query) |
            Q(invoice_number__icontains=query)
        )

    if checkin_from:
        bookings = bookings.filter(checkin_datetime__date__gte=checkin_from)

    if checkin_to:
        bookings = bookings.filter(checkin_datetime__date__lte=checkin_to)

    context = {
        "bookings": bookings,
        "query": query,
        "checkin_from": checkin_from,
        "checkin_to": checkin_to,
    }
    return render(request, 'checkin/checkin_checkout.html', context)

# ----------------- Update Checkout -----------------
def update_checkout(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.checkout_datetime and booking.checkout_datetime <= now():
        booking.status = 'completed'
        booking.save()
        if booking.room:
            booking.room.status = 'available'
            booking.room.save()
        ci, _ = CheckIn.objects.get_or_create(booking=booking)
        ci.status = 'checked_out'
        ci.save()

    if request.method == 'POST':
        form = UpdateCheckoutForm(request.POST, instance=booking)
        if form.is_valid():
            updated_booking = form.save()
            if updated_booking.status == 'completed' and updated_booking.room:
                updated_booking.room.status = 'available'
                updated_booking.room.save()
                ci, _ = CheckIn.objects.get_or_create(booking=updated_booking)
                ci.status = 'checked_out'
                ci.save()
            elif updated_booking.status in ['booked', 'pre-booked'] and updated_booking.room:
                updated_booking.room.status = 'occupied'
                updated_booking.room.save()
                ci, _ = CheckIn.objects.get_or_create(booking=updated_booking)
                ci.status = 'active'
                ci.save()
            return redirect('checkin_checkout:checkin_checkout')
        else:
            print(form.errors)
    else:
        form = UpdateCheckoutForm(instance=booking)

    return render(request, 'checkin/update_checkout.html', {'form': form, 'booking': booking})

# ----------------- Booking Details -----------------
from decimal import Decimal
from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from booking.models import Booking
from foods.models import FoodAndDrink

# ----------------- Booking Details -----------------
from django.shortcuts import render, get_object_or_404, redirect
from booking.models import Booking
from foods.models import FoodAndDrink
from decimal import Decimal
from collections import defaultdict


def booking_view_details(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    food_orders = FoodAndDrink.objects.filter(booking=booking)

    if request.method == 'POST':
        from checkin_checkout.forms import BookingUpdateForm
        form = BookingUpdateForm(request.POST, instance=booking)
        if form.is_valid():
            updated_booking = form.save()

            # Update room status
            if updated_booking.status == 'completed' and updated_booking.room:
                updated_booking.room.status = 'Available'
                updated_booking.room.save()
            elif updated_booking.status in ['booked', 'pre-booked'] and updated_booking.room:
                updated_booking.room.status = 'Occupied'
                updated_booking.room.save()

            return redirect('checkin_checkout:view_details', booking_id=booking.id)
    else:
        from checkin_checkout.forms import BookingUpdateForm
        form = BookingUpdateForm(instance=booking)

    # Calculate total days
    total_days = 0
    if booking.checkin_datetime and booking.checkout_datetime:
        total_days = (booking.checkout_datetime.date() - booking.checkin_datetime.date()).days
        if total_days < 0:
            total_days = 0

    # Room price and total
    room_price = Decimal(getattr(booking.room, 'price', 0) or 0)
    room_amount = room_price * Decimal(total_days)

    # GST Calculation
    cgst_rate = sgst_rate = Decimal('0.00')
    cgst_amount = sgst_amount = Decimal('0.00')
    if booking.apply_gst:
        gst_rate = Decimal('0.12') if room_amount < Decimal('7000.00') else Decimal('0.18')
        cgst_rate = sgst_rate = gst_rate / Decimal('2.0')
        cgst_amount = room_amount * cgst_rate
        sgst_amount = room_amount * sgst_rate
    else:
        gst_rate = Decimal('0.00')

    # Food details
    total_food_amount = Decimal('0.00')
    food_details = []
    for item in food_orders:
        food_price = Decimal(getattr(item, 'food_price', 0) or 0)
        drink_price = Decimal(getattr(item, 'drink_price', 0) or 0)
        quantity = Decimal(getattr(item, 'quantity', 1) or 1)
        subtotal = (food_price + drink_price) * quantity
        total_food_amount += subtotal

        food_details.append({
            'food_name': getattr(item, 'food_item', 'NA'),
            'drink_name': getattr(item, 'drink_item', 'NA'),
            'food_price': food_price,
            'drink_price': drink_price,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    # Grand total and balance
    grand_total = room_amount + cgst_amount + sgst_amount + total_food_amount
    amount_paid = booking.amount_paid or Decimal('0.00')
    balance_due = max(grand_total - amount_paid, Decimal('0.00'))

    apply_gst_display = "Yes" if booking.apply_gst else "No"

    context = {
        'booking': booking,
        'form': form,
        'food_details': food_details,
        'total_days': total_days,
        'room_price': room_price,
        'room_amount': room_amount,
        'total_food_amount': total_food_amount,
        'grand_total': grand_total,
        'apply_gst_display': apply_gst_display,
        'cgst_rate': cgst_rate * 100,  # display in %
        'sgst_rate': sgst_rate * 100,
        'cgst_amount': cgst_amount,
        'sgst_amount': sgst_amount,
        'amount_paid': amount_paid,
        'balance_due': balance_due,
    }
    return render(request, 'checkin/view_details.html', context)

# ----------------- Invoice -----------------
def invoice_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    food_orders = FoodAndDrink.objects.filter(booking=booking)

    # Total days
    total_days = max(0, (booking.checkout_datetime.date() - booking.checkin_datetime.date()).days) \
        if booking.checkin_datetime and booking.checkout_datetime else 0

    # Room pricing
    room_price = Decimal(getattr(booking.room, 'price', 0) or 0)
    room_amount = room_price * Decimal(total_days)

    # GST Calculation
    cgst_rate = sgst_rate = Decimal('0.00')
    cgst_amount = sgst_amount = Decimal('0.00')
    if booking.apply_gst:
        gst_rate = Decimal('0.12') if room_amount < Decimal('7000.00') else Decimal('0.18')
        cgst_rate = sgst_rate = gst_rate / Decimal('2.0')
        cgst_amount = room_amount * cgst_rate
        sgst_amount = room_amount * sgst_rate
    else:
        gst_rate = Decimal('0.00')

    # Food totals
    food_amount = Decimal('0.00')
    customer_orders = defaultdict(list)
    for item in food_orders:
        item_price = Decimal(getattr(item, 'food_price', 0) or 0)
        item_quantity = Decimal(getattr(item, 'quantity', 1) or 1)
        item.subtotal = item_price * item_quantity
        food_amount += item.subtotal
        item_name = getattr(item, 'food_item', None) or getattr(item, 'drink_item', None) or "N/A"
        customer_orders[booking.customer_name].append({
            'name': item_name,
            'price': item_price,
            'quantity': item_quantity,
            'subtotal': item.subtotal
        })

   
    grand_total = room_amount + cgst_amount + sgst_amount + food_amount
    amount_paid = booking.amount_paid or Decimal('0.00')
    balance_due = max(grand_total - amount_paid, Decimal('0.00'))

    context = {
        'booking': booking,
        'total_days': total_days,
        'room_price': room_price,
        'room_amount': room_amount,
        'gst_rate': gst_rate * 100,  # percentage
        'cgst_rate': cgst_rate * 100,
        'sgst_rate': sgst_rate * 100,
        'cgst_amount': cgst_amount,
        'sgst_amount': sgst_amount,
        'food_orders': food_orders,
        'customer_orders': dict(customer_orders),
        'food_amount': food_amount,
        'grand_total': grand_total,
        'amount_paid': amount_paid,
        'balance_due': balance_due,
        'payment_type': getattr(booking, 'payment_type', 'N/A').upper(),
        'invoice_number': getattr(booking, 'invoice_number', f"INV-{booking.id:06d}"),
    }
    return render(request, 'checkin/invoice.html', context)
