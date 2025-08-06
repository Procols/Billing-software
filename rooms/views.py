from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Room, Floor
from .forms import RoomForm, RoomUpdateForm

@login_required
def room_management(request):
    # Ensure floors exist (1 to 5 by default)
    for i in range(1, 6):
        Floor.objects.get_or_create(number=i)

    ac_count = Room.objects.filter(ac_type='AC').count()
    non_ac_count = Room.objects.filter(ac_type='Non-AC').count()
    maintenance_count = Room.objects.filter(status='Maintenance').count()

    # Handle add new room form
    if request.method == 'POST' and 'add_room' in request.POST:
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rooms:room_management')
    else:
        form = RoomForm()

    # Handle update room form
    if request.method == 'POST' and 'update_room' in request.POST:
        room_id = request.POST.get('room_id')
        room = get_object_or_404(Room, id=room_id)
        update_form = RoomUpdateForm(request.POST, instance=room)
        if update_form.is_valid():
            update_form.save()
            return redirect('rooms:room_management')
    else:
        update_form = RoomUpdateForm()

    context = {
        'ac_count': ac_count,
        'non_ac_count': non_ac_count,
        'maintenance_count': maintenance_count,
        'form': form,
        'update_form': update_form,
        'rooms': Room.objects.all(),
    }
    return render(request, 'rooms/room_management.html', context)
