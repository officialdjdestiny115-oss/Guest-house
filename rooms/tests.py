from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class RoomManagementTests(TestCase):
    def test_room_list_page_loads(self):
        user = get_user_model().objects.create_user(username='roomtester', password='secret123')
        self.client.force_login(user)

        response = self.client.get(reverse('room_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Room List')
