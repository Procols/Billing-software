from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, RoomType, Floor
from .forms import RoomTypeForm, RoomForm

@login_required
def room_management(request):
    for i in range(1, 6):
        Floor.objects.get_or_create(number=i)

    ac_count = Room.objects.filter(room_type__ac_type='ac').count()
    non_ac_count = Room.objects.filter(room_type__ac_type='non-ac').count()
    maintenance_count = Room.objects.filter(status='maintenance').count()

    room_type_form = RoomTypeForm(prefix='type')
    room_form = RoomForm(prefix='room')

    if request.method == 'POST':
        if 'type-submit' in request.POST:
            room_type_form = RoomTypeForm(request.POST, prefix='type')
            if room_type_form.is_valid():
                room_type_form.save()
                return redirect('rooms:room_management')
        elif 'room-submit' in request.POST:
            room_form = RoomForm(request.POST, prefix='room')
            if room_form.is_valid():
                room_form.save()
                return redirect('rooms:room_management')

    context = {
        'ac_count': ac_count,
        'non_ac_count': non_ac_count,
        'maintenance_count': maintenance_count,
        'room_type_form': room_type_form,
        'room_form': room_form,
        'room_types': RoomType.objects.all(),
        'rooms': Room.objects.all(),
    }
    return render(request, 'rooms/room_management.html', context)