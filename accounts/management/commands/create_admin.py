from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import StaffProfile


class Command(BaseCommand):
    help = 'Creates or resets the superadmin and admin accounts'

    def handle(self, *args, **options):

        # ── Super Admin ──────────────────────────────────────────
        super_user, created = User.objects.get_or_create(username='superadmin')
        super_user.email = 'superadmin@guesthouse.local'
        super_user.is_superuser = True
        super_user.is_staff = True
        super_user.is_active = True
        super_user.set_password('SuperAdmin@123')
        super_user.save()
        self.stdout.write(self.style.SUCCESS(
            f"[OK] superadmin {'created' if created else 'updated'} — password: SuperAdmin@123"
        ))

        # ── Admin User ───────────────────────────────────────────
        admin_user, created = User.objects.get_or_create(username='adminuser')
        admin_user.email = 'admin@guesthouse.local'
        admin_user.is_superuser = False
        admin_user.is_staff = True
        admin_user.is_active = True
        admin_user.set_password('AdminUser@123')
        admin_user.save()

        profile, _ = StaffProfile.objects.get_or_create(user=admin_user)
        profile.role = 'admin'
        profile.full_name = 'Admin User'
        profile.save()

        self.stdout.write(self.style.SUCCESS(
            f"[OK] adminuser {'created' if created else 'updated'} — password: AdminUser@123"
        ))

        self.stdout.write(self.style.SUCCESS('\nDone. Login at /admin/ or /admin-login/'))
