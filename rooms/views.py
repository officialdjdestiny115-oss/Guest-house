from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .models import Room


def is_room_manager(user):
    return user.is_superuser or (hasattr(user, 'staffprofile') and user.staffprofile.role == 'admin')


@login_required
@user_passes_test(is_room_manager)
def room_list(request):
    rooms = Room.objects.all().order_by('room_number')
    return render(request, 'rooms/list.html', {'rooms': rooms})


@login_required
@user_passes_test(is_room_manager)
def room_create(request):
    if request.method == 'POST':
        uploaded_image = request.FILES.get('image')
        room = Room(
            room_number=request.POST.get('room_number'),
            room_type=request.POST.get('room_type'),
            capacity=request.POST.get('capacity', 2),
            price_per_night=request.POST.get('price_per_night', 0),
            status=request.POST.get('status', 'available'),
            description=request.POST.get('description', ''),
            image=uploaded_image if uploaded_image else None,
            image_url=request.POST.get('image_url', ''),
        )
        room.save()
        return redirect('room_list')
    return render(request, 'rooms/form.html')


@login_required
@user_passes_test(is_room_manager)
def room_delete(request, room_id):
    if request.method == 'POST':
        room = Room.objects.filter(pk=room_id).first()
        if room:
            room.delete()
    return redirect('room_list')
