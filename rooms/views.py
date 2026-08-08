from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Room


@login_required
def room_list(request):
    rooms = Room.objects.all().order_by('room_number')
    return render(request, 'rooms/list.html', {'rooms': rooms})


@login_required
def room_create(request):
    if request.method == 'POST':
        room = Room(
            room_number=request.POST.get('room_number'),
            room_type=request.POST.get('room_type'),
            capacity=request.POST.get('capacity', 2),
            price_per_night=request.POST.get('price_per_night', 0),
            status=request.POST.get('status', 'available'),
            description=request.POST.get('description', ''),
        )
        room.save()
        return redirect('room_list')
    return render(request, 'rooms/form.html')
