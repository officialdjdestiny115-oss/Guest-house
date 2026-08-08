from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class BookingManagementTests(TestCase):
    def test_booking_create_page_loads(self):
        user = get_user_model().objects.create_user(username='bookingtester', password='secret123')
        self.client.force_login(user)

        response = self.client.get(reverse('booking_create'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Booking')
