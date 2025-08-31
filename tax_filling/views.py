from django.shortcuts import render
from django.utils.timezone import now, timedelta
from booking.models import Booking
from .forms import TaxFilterForm
from decimal import Decimal


def tax_filing_view(request):
    form = TaxFilterForm(request.GET or None)
    bookings = Booking.objects.filter(apply_gst=True)

    # --- Apply Filters ---
    if form.is_valid():
        invoice = form.cleaned_data.get("invoice")
        from_date = form.cleaned_data.get("from_date")
        to_date = form.cleaned_data.get("to_date")
        min_gst = form.cleaned_data.get("min_gst")
        max_gst = form.cleaned_data.get("max_gst")

        if invoice:
            bookings = bookings.filter(invoice_number__icontains=invoice)
        if from_date:
            bookings = bookings.filter(created_at__date__gte=from_date)
        if to_date:
            bookings = bookings.filter(created_at__date__lte=to_date)
        if min_gst is not None:
            bookings = [b for b in bookings if (b.cgst_amount + b.sgst_amount) >= min_gst]
        if max_gst is not None:
            bookings = [b for b in bookings if (b.cgst_amount + b.sgst_amount) <= max_gst]

    # --- Summary values ---
    today = now().date()
    last_7_days = today - timedelta(days=7)
    last_15_days = today - timedelta(days=15)
    last_30_days = today - timedelta(days=30)

    def gst_total(since_date):
        qs = Booking.objects.filter(apply_gst=True, created_at__date__gte=since_date)
        return sum([(b.cgst_amount + b.sgst_amount) for b in qs], Decimal(0))

    summary = {
        "last7": gst_total(last_7_days),
        "last15": gst_total(last_15_days),
        "last30": gst_total(last_30_days),
    }

    context = {
        "form": form,
        "bookings": bookings,
        "summary": summary,
    }
    return render(request, "tax_filling/tax_filling.html", context)
