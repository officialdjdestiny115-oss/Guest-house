from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rooms.models import Room
from .models import Booking


@login_required
def booking_create(request):
    rooms = Room.objects.filter(status='available').order_by('room_number')
    message = None
    form_data = {
        'guest_name': '',
        'guest_phone': '',
        'check_in': '',
        'nights': 1,
        'adults': 1,
        'children': 0,
        'notes': '',
        'selected_room_id': None,
    }
    total_cost = 0

    selected_room_id = request.GET.get('room') or None
    if selected_room_id:
        form_data['selected_room_id'] = selected_room_id

    if request.method == 'POST':
        form_data.update({
            'guest_name': request.POST.get('guest_name', '').strip(),
            'guest_phone': request.POST.get('guest_phone', '').strip(),
            'check_in': request.POST.get('check_in', ''),
            'nights': request.POST.get('nights', 1) or 1,
            'adults': request.POST.get('adults', 1) or 1,
            'children': request.POST.get('children', 0) or 0,
            'notes': request.POST.get('notes', '').strip(),
            'selected_room_id': request.POST.get('room'),
        })

        room_id = form_data['selected_room_id']
        check_in_str = form_data['check_in']
        try:
            nights = int(form_data['nights'])
        except (TypeError, ValueError):
            nights = 0

        if room_id and check_in_str and nights > 0:
            try:
                check_in_date = date.fromisoformat(check_in_str)
            except ValueError:
                message = 'Please select a valid check-in date.'
            else:
                if check_in_date < date.today():
                    message = 'Check-in date cannot be in the past.'
                else:
                    check_out_date = check_in_date + timedelta(days=nights)
                    room = Room.objects.filter(pk=room_id, status='available').first()
                    if room is None:
                        message = 'Selected room is not available. Please choose another one.'
                    else:
                        total_cost = room.price_per_night * nights
                        booking = Booking(
                            guest_name=form_data['guest_name'],
                            guest_phone=form_data['guest_phone'],
                            room=room,
                            check_in=check_in_date,
                            check_out=check_out_date,
                            adults=int(form_data['adults'] or 1),
                            children=int(form_data['children'] or 0),
                            status='pending',
                            notes=form_data['notes'],
                        )
                        booking.save()
                        room.status = 'reserved'
                        room.save()
                        return redirect('dashboard')
        else:
            message = 'Please select an available room and choose how long you will stay.'

    return render(
        request,
        'bookings/form.html',
        {
            'rooms': rooms,
            'message': message,
            'form_data': form_data,
            'total_cost': total_cost,
        },
    )
