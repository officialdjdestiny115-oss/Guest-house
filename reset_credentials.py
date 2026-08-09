"""
reset_credentials.py
--------------------
Resets / creates the superadmin and adminuser accounts with known credentials.
Run with:  python reset_credentials.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'guesthouse_system.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import StaffProfile

# ──────────────────────────────────────────────
# Credentials — change these if you want
# ──────────────────────────────────────────────
SUPER_ADMIN = {
    'username': 'superadmin',
    'password': 'SuperAdmin@123',
    'email': 'superadmin@guesthouse.local',
}

ADMIN_USER = {
    'username': 'adminuser',
    'password': 'AdminUser@123',
    'email': 'admin@guesthouse.local',
    'full_name': 'Admin User',
}
# ──────────────────────────────────────────────


def reset_superadmin():
    user, created = User.objects.get_or_create(username=SUPER_ADMIN['username'])
    user.email = SUPER_ADMIN['email']
    user.is_superuser = True
    user.is_staff = True
    user.is_active = True
    user.set_password(SUPER_ADMIN['password'])
    user.save()
    action = 'Created' if created else 'Updated'
    print(f"[OK] {action} superadmin account")
    print(f"     Username : {SUPER_ADMIN['username']}")
    print(f"     Password : {SUPER_ADMIN['password']}")
    print(f"     URL      : http://127.0.0.1:8000/admin/")


def reset_adminuser():
    user, created = User.objects.get_or_create(username=ADMIN_USER['username'])
    user.email = ADMIN_USER['email']
    user.is_superuser = False
    user.is_staff = True
    user.is_active = True
    user.set_password(ADMIN_USER['password'])
    user.save()

    # Ensure StaffProfile exists and is set to 'admin' role
    profile, _ = StaffProfile.objects.get_or_create(user=user)
    profile.role = 'admin'
    profile.full_name = ADMIN_USER['full_name']
    profile.save()

    action = 'Created' if created else 'Updated'
    print(f"\n[OK] {action} admin account")
    print(f"     Username : {ADMIN_USER['username']}")
    print(f"     Password : {ADMIN_USER['password']}")
    print(f"     URL      : http://127.0.0.1:8000/admin-login/")


if __name__ == '__main__':
    print("=" * 50)
    print("  Guest House — Credential Reset")
    print("=" * 50)
    reset_superadmin()
    reset_adminuser()
    print("\n" + "=" * 50)
    print("  Done. Start the server with:")
    print("  python manage.py runserver")
    print("=" * 50)
