from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import StaffProfile, GuestProfile


class StaffProfileInline(admin.StackedInline):
    model = StaffProfile
    can_delete = False
    verbose_name_plural = 'Staff Profile'
    extra = 0


class GuestProfileInline(admin.StackedInline):
    model = GuestProfile
    can_delete = False
    verbose_name_plural = 'Guest Profile'
    extra = 0


class CustomUserAdmin(UserAdmin):
    inlines = [StaffProfileInline, GuestProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active']
    list_filter = ['is_staff', 'is_superuser', 'is_active']


# Re-register User with the custom admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'role', 'phone', 'national_id']
    list_filter = ['role']
    search_fields = ['user__username', 'full_name', 'national_id']


@admin.register(GuestProfile)
class GuestProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'last_name', 'phone', 'national_id']
    search_fields = ['user__username', 'full_name', 'national_id']
