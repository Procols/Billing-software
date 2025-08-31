from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Booking
from .forms import BookingForm
from django.contrib.auth.decorators import login_required
from rooms.models import Room
from checkin_checkout.models import CheckIn
from django.utils.timezone import now



@login_required
def booking_list(request):
    # Search filter
    query = request.GET.get("q", "")
    status_filter = request.GET.get("status", "all")

    bookings = Booking.objects.select_related("room")

    # Apply search filter
    if query:
        bookings = bookings.filter(
            Q(customer_name__icontains=query)
            | Q(phone_number__icontains=query)
            | Q(invoice_number__icontains=query)
            | Q(room__room_number__icontains=query)
        )

    # Apply status filter
    if status_filter == "booked":
        bookings = bookings.filter(status="booked")
    elif status_filter == "pre-booked":
        bookings = bookings.filter(status="pre-booked")

    bookings = bookings.order_by("-created_at")

    return render(
        request,
        "booking/booking_list.html",
        {
            "bookings": bookings,
            "query": query,
            "status_filter": status_filter,
        },
    )


@login_required
def new_booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            # create or update CheckIn record
            CheckIn.objects.update_or_create(
                booking=booking, defaults={"status": "active"}
            )
            return redirect("booking:booking_list")
    else:
        form = BookingForm()
    rooms = Room.objects.filter(status__iexact="Available").order_by("room_number")
    return render(request, "booking/new_booking.html", {"form": form, "rooms": rooms})


@login_required
def get_room_details(request):
    room_id = request.GET.get("room_id")
    try:
        room = Room.objects.get(id=room_id)
        data = {
            "room_type": room.room_type,
            "ac_type": getattr(room, "ac_type", ""),
            "floor": str(room.floor) if room.floor else "",
            "status": room.status,
            "price": float(room.price),
        }
        return JsonResponse(data)
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=404)
