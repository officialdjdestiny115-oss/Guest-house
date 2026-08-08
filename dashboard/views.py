from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from accounts.models import GuestProfile, StaffProfile
from bookings.models import Booking
from rooms.models import Room


def get_display_rooms():
    rooms = list(Room.objects.all().order_by('room_number'))
    if rooms:
        return rooms

    sample_images = ['room1.jfif', 'room2.jfif', 'room3.jfif', 'room4.jfif']
    return [
        {
            'room_number': f'G0{index}',
            'room_type': 'Deluxe Suite' if index % 2 == 0 else 'Executive Room',
            'capacity': 2,
            'price_per_night': 120 + index * 20,
            'status': 'available',
            'description': 'Bright, calm, and beautifully styled for a memorable stay.',
            'image_url': f'/images/{image_name}',
        }
        for index, image_name in enumerate(sample_images, start=1)
    ]


@login_required
def dashboard(request):
    rooms = Room.objects.all()
    bookings = Booking.objects.all().order_by('-id')[:5]
    stats = {
        'total_rooms': rooms.count(),
        'available_rooms': rooms.filter(status='available').count(),
        'occupied_rooms': rooms.filter(status='occupied').count(),
        'revenue': 125000,
    }
    context = {
        'stats': stats,
        'rooms': rooms,
        'recent_bookings': bookings,
        'user_role': getattr(request.user, 'staffprofile', None).role if hasattr(request.user, 'staffprofile') else 'admin',
    }
    if request.user.is_superuser:
        return render(request, 'dashboard/admin_dashboard.html', context)
    if hasattr(request.user, 'staffprofile') and request.user.staffprofile.role == 'receptionist':
        return render(request, 'dashboard/reception_dashboard.html', context)
    if hasattr(request.user, 'staffprofile') and request.user.staffprofile.role == 'admin':
        return render(request, 'dashboard/admin_dashboard.html', context)
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
def guest_dashboard(request):
    rooms = get_display_rooms()
    return render(request, 'dashboard/guest_dashboard.html', {'rooms': rooms})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password1', '').strip()
        if username and password:
            user = User.objects.create_user(username=username, password=password)
            GuestProfile.objects.create(
                user=user,
                full_name=request.POST.get('full_name', ''),
                last_name=request.POST.get('last_name', ''),
                phone=request.POST.get('phone', ''),
                national_id=request.POST.get('national_id', ''),
            )
            login(request, user)
            return redirect('guest_dashboard')
    return render(request, 'accounts/register.html')


def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('super_admin_dashboard')
        if hasattr(request.user, 'staffprofile'):
            return redirect('dashboard')
        return redirect('guest_dashboard')
    return render(request, 'dashboard/landing.html')


def availability(request):
    rooms = get_display_rooms()
    return render(request, 'dashboard/availability.html', {'rooms': rooms})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def super_admin_dashboard(request):
    message = None
    if request.method == 'POST' and request.POST.get('action') == 'create_admin':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        national_id = request.POST.get('national_id', '').strip()
        if username and password:
            if User.objects.filter(username=username).exists():
                message = f'Username "{username}" already exists.'
            else:
                user = User.objects.create_user(username=username, password=password, is_staff=True)
                StaffProfile.objects.create(user=user, role='admin', full_name=full_name, phone=phone, national_id=national_id)
                message = f'Admin account "{username}" created successfully.'
    rooms = Room.objects.all()
    admins = User.objects.filter(is_staff=True).exclude(is_superuser=True)
    stats = {
        'total_rooms': rooms.count(),
        'available_rooms': rooms.filter(status='available').count(),
        'occupied_rooms': rooms.filter(status='occupied').count(),
    }
    return render(request, 'dashboard/superadmin/overview.html', {'admins': admins, 'stats': stats, 'message': message})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def super_admin_users(request):
    message = None
    if request.method == 'POST' and request.POST.get('action') == 'delete_admin':
        admin_id = request.POST.get('admin_id')
        admin_user = User.objects.filter(id=admin_id, is_staff=True, is_superuser=False).first()
        if admin_user:
            admin_user.delete()
            message = f'Admin account "{admin_user.username}" removed successfully.'
    admins = User.objects.filter(is_staff=True).exclude(is_superuser=True)
    return render(request, 'dashboard/superadmin/users.html', {'admins': admins, 'message': message})


@login_required
@user_passes_test(lambda user: user.is_superuser or hasattr(user, 'staffprofile'))
def guest_list(request):
    message = None
    if request.method == 'POST' and request.POST.get('action') == 'delete_guest':
        guest_id = request.POST.get('guest_id')
        guest_user = User.objects.filter(id=guest_id, is_staff=False, is_superuser=False).first()
        if guest_user and hasattr(guest_user, 'guestprofile'):
            guest_user.delete()
            message = f'Guest "{guest_user.username}" has been removed.'
    guests = GuestProfile.objects.select_related('user').all().order_by('user__date_joined')
    return render(request, 'dashboard/guest_list.html', {'guests': guests, 'message': message})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def super_admin_rooms(request):
    rooms = Room.objects.all().order_by('room_number')
    return render(request, 'dashboard/superadmin/rooms.html', {'rooms': rooms})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def super_admin_bookings(request):
    bookings = Booking.objects.all().order_by('-id')
    return render(request, 'dashboard/superadmin/bookings.html', {'bookings': bookings})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def super_admin_logs(request):
    rooms = Room.objects.all()
    bookings = Booking.objects.all()
    return render(request, 'dashboard/superadmin/logs.html', {'rooms': rooms, 'bookings': bookings})
