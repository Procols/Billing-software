from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Room, Floor
from .forms import RoomForm, RoomUpdateForm
from django.contrib.auth.decorators import login_required

@login_required
def room_management(request):
    # ensure floors 1..5 exist
    for i in range(1, 6):
        Floor.objects.get_or_create(number=i)

    ac_count = Room.objects.filter(ac_type='AC').count()
    non_ac_count = Room.objects.filter(ac_type='Non-AC').count()
    maintenance_count = Room.objects.filter(status='Maintenance').count()

    # add
    if request.method == 'POST' and request.POST.get('action') == 'add':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Room added.")
            return redirect('rooms:room_management')
    else:
        form = RoomForm()

    # update
    if request.method == 'POST' and request.POST.get('action') == 'update':
        room_id = request.POST.get('room_id')
        room = get_object_or_404(Room, id=room_id)
        update_form = RoomUpdateForm(request.POST, instance=room)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, "Room updated.")
            return redirect('rooms:room_management')
    else:
        update_form = RoomUpdateForm()

    # delete
    if request.method == 'POST' and request.POST.get('action') == 'delete':
        room_id = request.POST.get('room_id')
        room = get_object_or_404(Room, id=room_id)
        room.delete()
        messages.success(request, "Room deleted.")
        return redirect('rooms:room_management')

    rooms = Room.objects.select_related('floor').order_by('room_number')
    context = {
        'ac_count': ac_count,
        'non_ac_count': non_ac_count,
        'maintenance_count': maintenance_count,
        'form': form,
        'update_form': update_form,
        'rooms': rooms,
        'room_type_choices': Room.ROOM_TYPE_CHOICES,
        'ac_type_choices': Room.AC_CHOICES,
        'status_choices': Room.STATUS_CHOICES,
        'floors': Floor.objects.all().order_by('number'),
    }
    return render(request, 'rooms/room_management.html', context)
