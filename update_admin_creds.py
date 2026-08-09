import os
import django
from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'guesthouse_system.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

SUPERADMIN_USERNAME = 'superadmin'
SUPERADMIN_PASSWORD = 'SuperAdmin!234'
ADMIN_USERNAME = 'adminuser'
ADMIN_PASSWORD = 'AdminUser!234'

with transaction.atomic():
    superuser, created = User.objects.get_or_create(
        username=SUPERADMIN_USERNAME,
        defaults={'is_superuser': True, 'is_staff': True},
    )
    superuser.is_superuser = True
    superuser.is_staff = True
    superuser.set_password(SUPERADMIN_PASSWORD)
    superuser.save()

    admin_user, created = User.objects.get_or_create(
        username=ADMIN_USERNAME,
        defaults={'is_superuser': False, 'is_staff': True},
    )
    admin_user.is_superuser = False
    admin_user.is_staff = True
    admin_user.set_password(ADMIN_PASSWORD)
    admin_user.save()

print('Superadmin account:')
print('  username:', SUPERADMIN_USERNAME)
print('  password:', SUPERADMIN_PASSWORD)
print('Admin account:')
print('  username:', ADMIN_USERNAME)
print('  password:', ADMIN_PASSWORD)
