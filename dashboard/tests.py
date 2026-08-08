from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DashboardViewTests(TestCase):
    def test_dashboard_page_loads(self):
        user = get_user_model().objects.create_user(username='tester', password='secret123')
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Dashboard')

    def test_guest_registration_creates_user_and_redirects(self):
        response = self.client.post(
            reverse('register'),
            {'username': 'guestuser', 'email': 'guest@example.com', 'password1': 'StrongPass123!', 'password2': 'StrongPass123!'},
            follow=True,
        )

        self.assertRedirects(response, reverse('guest_dashboard'))
        self.assertTrue(get_user_model().objects.filter(username='guestuser').exists())

    def test_super_admin_can_create_admin_account(self):
        superuser = get_user_model().objects.create_superuser(username='superadmin', password='superpass123')
        self.client.force_login(superuser)

        response = self.client.post(
            reverse('super_admin_dashboard'),
            {'username': 'newadmin', 'password': 'AdminPass123!', 'action': 'create_admin'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(get_user_model().objects.filter(username='newadmin', is_staff=True).exists())
