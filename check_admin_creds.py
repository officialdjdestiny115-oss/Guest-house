import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'guesthouse_system.settings')
django.setup()

from django.contrib.auth import get_user_model, authenticate
User = get_user_model()

for username, password in [('superadmin', 'SuperAdmin!234'), ('adminuser', 'AdminUser!234')]:
    user = User.objects.filter(username=username).first()
    print('Username:', username)
    print('  exists:', bool(user))
    if user:
        print('  is_superuser:', user.is_superuser)
        print('  is_staff:', user.is_staff)
        print('  is_active:', user.is_active)
        print('  password hash:', user.password[:8])
    auth = authenticate(username=username, password=password)
    print('  authenticate:', bool(auth))
    print('---')
