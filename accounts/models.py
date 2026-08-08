from django.db import models
from django.contrib.auth.models import User


class StaffProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('receptionist', 'Receptionist'),
        ('manager', 'Manager'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='receptionist')
    phone = models.CharField(max_length=20, blank=True)
    full_name = models.CharField(max_length=100, blank=True)
    national_id = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.full_name or self.user.get_full_name() or self.user.username


class GuestProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    national_id = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.full_name or self.user.username
