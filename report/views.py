from django.shortcuts import render
from booking.models import Booking
from .forms import ReportFilterForm
from django.db.models import Sum
import openpyxl
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from accounts.decorators import admins_only

@admins_only
def booking_report(request):
    bookings = Booking.objects.all()
    form = ReportFilterForm(request.GET or None)

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        payment_status = form.cleaned_data.get('payment_status')

        if start_date:
            bookings = bookings.filter(checkin_datetime__date__gte=start_date)
        if end_date:
            bookings = bookings.filter(checkout_datetime__date__lte=end_date)
        if payment_status:
            bookings = bookings.filter(payment_status=payment_status)

    total_bookings = bookings.count()
    active_members = bookings.filter(payment_status='paid').values('customer_name').distinct().count()
    total_revenue = bookings.filter(payment_status='paid').aggregate(Sum('price'))['price__sum'] or 0
    cancelled_bookings = bookings.filter(payment_status='cancelled').count()

    # Export to Excel
    if 'export_excel' in request.GET:
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=booking_report.xlsx'
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Bookings"

        headers = ['Invoice ID', 'Guest Name', 'Room Number', 'Check-in', 'Check-out',
                   'Total Persons', 'CGST 6%', 'SGST 6%', 'Total Amount', 'Amount Paid', 'Payment Status']
        sheet.append(headers)

        for b in bookings:
            sheet.append([
                b.invoice_number,
                b.customer_name,
                b.room.room_number if b.room else "-",
                b.checkin_datetime.strftime('%Y-%m-%d'),
                b.checkout_datetime.strftime('%Y-%m-%d') if b.checkout_datetime else '-',
                b.total_persons,
                float(b.cgst_amount),
                float(b.sgst_amount),
                float(b.price),
                float(b.amount_paid),
                b.payment_status.capitalize()
            ])
        workbook.save(response)
        return response

    # Export to PDF
    if 'export_pdf' in request.GET:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=booking_report.pdf'

        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph("Booking Report", styles['Heading1']))
        elements.append(Spacer(1, 12))

        data = [['Invoice ID', 'Guest Name', 'Room Number', 'Check-in', 'Check-out',
                 'Total Persons', 'CGST 6%', 'SGST 6%', 'Total Amount', 'Amount Paid', 'Payment Status']]
        for b in bookings:
            data.append([
                b.invoice_number,
                b.customer_name,
                b.room.room_number if b.room else "-",
                b.checkin_datetime.strftime('%Y-%m-%d'),
                b.checkout_datetime.strftime('%Y-%m-%d') if b.checkout_datetime else '-',
                b.total_persons,
                f"₹{b.cgst_amount}",
                f"₹{b.sgst_amount}",
                f"₹{b.price}",
                f"₹{b.amount_paid}",
                b.payment_status.capitalize()
            ])

        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        doc.build(elements)
        return response

    context = {
        'form': form,
        'bookings': bookings,
        'total_bookings': total_bookings,
        'active_members': active_members,
        'total_revenue': total_revenue,
        'cancelled_bookings': cancelled_bookings,
    }
    return render(request, 'report/booking_report.html', context)
