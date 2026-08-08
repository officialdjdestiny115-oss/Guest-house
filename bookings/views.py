from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rooms.models import Room
from .models import Booking


@login_required
def booking_create(request):
    rooms = Room.objects.filter(status='available').order_by('room_number')
    if request.method == 'POST':
        room_id = request.POST.get('room')
        if room_id:
            room = Room.objects.get(pk=room_id)
            booking = Booking(
                guest_name=request.POST.get('guest_name', '').strip(),
                guest_phone=request.POST.get('guest_phone', '').strip(),
                room=room,
                check_in=request.POST.get('check_in'),
                check_out=request.POST.get('check_out'),
                adults=int(request.POST.get('adults', 1) or 1),
                children=int(request.POST.get('children', 0) or 0),
                status='pending',
                notes=request.POST.get('notes', '').strip(),
            )
            booking.save()
            room.status = 'reserved'
            room.save()
            return redirect('dashboard')
    return render(request, 'bookings/form.html', {'rooms': rooms})
