"""
URL configuration for guesthouse_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from dashboard.views import availability, dashboard, guest_dashboard, guest_list, home, register, super_admin_bookings, super_admin_dashboard, super_admin_logs, super_admin_rooms, super_admin_users
from rooms.views import room_list, room_create, room_delete
from bookings.views import booking_create

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('availability/', availability, name='availability'),
    path('dashboard/', dashboard, name='dashboard'),
    path('admin-dashboard/', dashboard, name='admin_dashboard'),
    path('guest-dashboard/', guest_dashboard, name='guest_dashboard'),
    path('guests/', guest_list, name='guest_list'),
    path('super-admin/', super_admin_dashboard, name='super_admin_dashboard'),
    path('super-admin/users/', super_admin_users, name='super_admin_users'),
    path('super-admin/rooms/', super_admin_rooms, name='super_admin_rooms'),
    path('super-admin/bookings/', super_admin_bookings, name='super_admin_bookings'),
    path('super-admin/logs/', super_admin_logs, name='super_admin_logs'),
    path('rooms/', room_list, name='room_list'),
    path('rooms/new/', room_create, name='room_create'),
    path('rooms/<int:room_id>/delete/', room_delete, name='room_delete'),
    path('bookings/new/', booking_create, name='booking_create'),
    path('admin-login/', auth_views.LoginView.as_view(template_name='accounts/admin_login.html'), name='admin_login'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
