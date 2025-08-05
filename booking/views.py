from django.shortcuts import render, redirect
from .models import Booking
from rooms.models import Room
from django.http import JsonResponse

def booking_list(request):
    bookings = Booking.objects.all()  # Get all bookings
    rooms = Room.objects.filter(status="available")  # Only available rooms
    return render(request, "booking/booking_list.html", {"bookings": bookings, "rooms": rooms})

def new_booking(request):
    if request.method == "POST":
        customer_name = request.POST["customer_name"]
        phone_number = request.POST["phone_number"]
        address = request.POST.get("address", "")
        document_type = request.POST["document_type"]
        document_number = request.POST["document_number"]
        room_id = request.POST["room"]
        adults = request.POST["adults"]
        children = request.POST["children"]
        booking_status = request.POST["booking_status"]
        checkin_date = request.POST["checkin_date"]
        checkout_date = request.POST["checkout_date"]
        payment_type = request.POST["payment_type"]
        apply_gst = request.POST.get("apply_gst") == "true"

        room = Room.objects.get(id=room_id)

        # Create booking WITHOUT invoice_number - model will set it automatically
        booking = Booking.objects.create(
            customer_name=customer_name,
            phone_number=phone_number,
            address=address,
            document_type=document_type,
            document_number=document_number,
            room=room,
            adults=adults,
            children=children,
            booking_status=booking_status,
            checkin_date=checkin_date,
            checkout_date=checkout_date,
            payment_type=payment_type,
            apply_gst=apply_gst,
        )

        # Mark room as booked
        room.status = "booked"
        room.save()

        return redirect("booking:booking_list")

    rooms = Room.objects.filter(status="available")
    return render(request, "booking/new_booking.html", {"rooms": rooms})

def get_room_details(request):
    room_id = request.GET.get("room_id")
    try:
        room = Room.objects.get(id=room_id)
        data = {
            "room_type": room.room_type,
            "ac_type": room.ac_type,
            "floor": room.floor,
            "status": room.status,
            "price": float(room.price),
        }
        return JsonResponse(data)
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=404)
