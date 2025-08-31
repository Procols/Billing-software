from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from booking.models import Booking
from .forms import PaymentFilterForm

def payment_list(request):
    # Initialize the form with GET data
    form = PaymentFilterForm(request.GET or None)

    # Start with all bookings that have a payment type
    payments = Booking.objects.exclude(payment_type__isnull=True)

    # Apply filters if form is valid
    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        payment_mode = form.cleaned_data.get('payment_mode')

        if start_date:
            payments = payments.filter(checkin_datetime__date__gte=start_date)
        if payment_mode:
            payments = payments.filter(payment_type=payment_mode)

    # Calculate totals
    today = timezone.now().date()
    last_7_days = today - timedelta(days=7)
    last_15_days = today - timedelta(days=15)
    last_30_days = today - timedelta(days=30)

    last_7_days_income = payments.filter(checkin_datetime__date__gte=last_7_days).aggregate(
        total=Sum('price'))['total'] or 0
    last_15_days_income = payments.filter(checkin_datetime__date__gte=last_15_days).aggregate(
        total=Sum('price'))['total'] or 0
    last_30_days_income = payments.filter(checkin_datetime__date__gte=last_30_days).aggregate(
        total=Sum('price'))['total'] or 0

    cash_total = payments.filter(payment_type='cash').aggregate(total=Sum('price'))['total'] or 0
    upi_total = payments.filter(payment_type='upi').aggregate(total=Sum('price'))['total'] or 0
    card_total = payments.filter(payment_type='card').aggregate(total=Sum('price'))['total'] or 0

    context = {
        'form': form,
        'payments': payments.order_by('-checkin_datetime'),
        'last_7_days_income': last_7_days_income,
        'last_15_days_income': last_15_days_income,
        'last_30_days_income': last_30_days_income,
        'cash_total': cash_total,
        'upi_total': upi_total,
        'card_total': card_total,
    }

    return render(request, 'transaction/payment_list.html', context)
