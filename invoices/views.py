from django.shortcuts import render, get_object_or_404
from booking.models import Booking
from .forms import InvoiceFilterForm
from decimal import Decimal

def invoice_list(request):
    form = InvoiceFilterForm(request.GET or None)
    bookings = Booking.objects.select_related('room').order_by('-created_at')

    if form.is_valid():
        invoice_number = form.cleaned_data.get('invoice_number')
        guest_name = form.cleaned_data.get('guest_name')
        status = form.cleaned_data.get('status')

        if invoice_number:
            bookings = bookings.filter(invoice_number__icontains=invoice_number)
        if guest_name:
            bookings = bookings.filter(customer_name__icontains=guest_name)
        if status:
            bookings = bookings.filter(payment_status=status)

    return render(request, 'invoices/invoice_list.html', {'bookings': bookings, 'form': form})

from django.shortcuts import render, get_object_or_404
from .models import Booking # if you have a food order model

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

    # Food orders (optional)
    
    # Grand total
    
    grand_total = room_amount + cgst_amount + sgst_amount 
    amount_paid = booking.amount_paid or Decimal('0.00')
    balance_due = max(grand_total - amount_paid, Decimal('0.00'))
    return render(request, 'invoices/invoice_detail.html', {
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
