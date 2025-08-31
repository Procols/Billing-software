from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from decimal import Decimal

from rooms.models import Room
from booking.models import Booking
from .forms import InvoiceFilterForm


@login_required
def dashboard(request):
    today = timezone.localdate()

    # Total rooms
    total_rooms = Room.objects.count()

    # Rooms occupied today
    occupied_bookings = Booking.objects.filter(
        checkin_datetime__date__lte=today
    ).filter(
        Q(checkout_datetime__isnull=True) | Q(checkout_datetime__date__gt=today)
    )

    occupied_rooms = occupied_bookings.values('room_id').distinct().count()
    available_rooms = max(total_rooms - occupied_rooms, 0)
    occupancy_rate = round((occupied_rooms / total_rooms) * 100, 2) if total_rooms else 0.0

    # Today’s metrics
    todays_bookings = Booking.objects.filter(created_at__date=today).count()
    todays_checkins = Booking.objects.filter(checkin_datetime__date=today).count()
    todays_revenue = Booking.objects.filter(
        created_at__date=today,
        payment_status="paid"
    ).aggregate(total=Sum('price'))['total'] or 0

    # Invoice filter form
    form = InvoiceFilterForm(request.GET or None)
    invoices = Booking.objects.select_related('room').order_by('-created_at')

    if form.is_valid():
        invoice_number = form.cleaned_data.get('invoice_number')
        guest_name = form.cleaned_data.get('guest_name')
        status = form.cleaned_data.get('status')

        if invoice_number:
            invoices = invoices.filter(invoice_number__icontains=invoice_number)
        if guest_name:
            invoices = invoices.filter(customer_name__icontains=guest_name)
        if status:
            invoices = invoices.filter(payment_status=status)

    context = {
        "total_rooms": total_rooms,
        "occupied_rooms": occupied_rooms,
        "available_rooms": available_rooms,
        "occupancy_rate": occupancy_rate,
        "todays_bookings": todays_bookings,
        "todays_checkins": todays_checkins,
        "todays_revenue": todays_revenue,
        "bookings": invoices,  # pass filtered invoices to dashboard
        "form": form,
    }

    return render(request, "core/dashboard.html", context)


@login_required
def invoice_detail(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)

    # Calculate number of days stayed
    if booking.checkout_datetime and booking.checkin_datetime:
        delta = booking.checkout_datetime.date() - booking.checkin_datetime.date()
        total_days = delta.days if delta.days > 0 else 1
    else:
        total_days = 1

    # Room rent calculations
    room_price = booking.room.price  # per day
    room_amount = room_price * total_days

    # GST calculation
    gst_rate = 12 if room_amount < 7000 else 18
    cgst_amount = (room_amount * gst_rate / 2) / 100
    sgst_amount = (room_amount * gst_rate / 2) / 100

    # Grand total
    grand_total = room_amount + cgst_amount + sgst_amount 
    amount_paid = booking.amount_paid or Decimal('0.00')
    balance_due = max(grand_total - amount_paid, Decimal('0.00'))

    return render(request, 'core/invoice_detail.html', {
        'booking': booking,
        'total_days': total_days,
        'room_price': room_price,
        'room_amount': room_amount,
        'gst_rate': gst_rate,
        'cgst_amount': cgst_amount,
        'sgst_amount': sgst_amount,
        'grand_total': grand_total,
        'payment_type': booking.payment_type,
        'invoice_number': booking.invoice_number,
        'amount_paid': amount_paid,
        'balance_due': balance_due,
    })
