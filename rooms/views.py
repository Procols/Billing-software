from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Floor
from .forms import RoomForm

@login_required
def room_management(request):
    # Ensure floors exist (1 to 5 by default)
    for i in range(1, 6):
        Floor.objects.get_or_create(number=i)

    ac_count = Room.objects.filter(ac_type='AC').count()
    non_ac_count = Room.objects.filter(ac_type='Non-AC').count()
    maintenance_count = Room.objects.filter(status='Maintenance').count()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rooms:room_management')
    else:
        form = RoomForm()

    context = {
        'ac_count': ac_count,
        'non_ac_count': non_ac_count,
        'maintenance_count': maintenance_count,
        'form': form,
        'rooms': Room.objects.all(),
    }
    return render(request, 'rooms/room_management.html', context)
