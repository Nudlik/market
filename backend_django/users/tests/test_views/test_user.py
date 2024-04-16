from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class UserViewSetTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(email='1@1.ru', phone='+7123')
        self.user.set_password('1111')
        self.user.is_active = True
        self.user.save()

    def test_create_user(self):
        data = {
            'email': 'test2@example.com',
            'password': 'testpassword',
            'phone': '+71234567890'
        }
        url = reverse('users-list')
        response = self.client.post(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 2)

    def test_get_user(self):
        url = reverse('users-list')
        self.client.force_login(self.user)
        response = self.client.get(url)
        results = response.json()['results'][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 4)
        self.assertEqual(results['email'], self.user.email)
        self.assertEqual(results['phone'], self.user.phone)
        self.assertEqual(results['first_name'], self.user.first_name)
        self.assertEqual(results['last_name'], self.user.last_name)
        self.assertEqual(results['phone'], self.user.phone)
        self.assertIsNone(results['image'])

    def test_update_user(self):
        data = {
            'first_name': 'My_first_name',
        }
        url = reverse('users-me')
        self.client.force_login(self.user)
        response = self.client.patch(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        updated_user = get_user_model().objects.get(id=self.user.id)
        self.assertEqual(updated_user.first_name, 'My_first_name')

    def test_delete_user(self):
        data = {
            'email': self.user.email,
            'phone': self.user.phone,
        }
        url = reverse('users-me')
        self.client.force_login(self.user)
        response = self.client.delete(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(get_user_model().objects.count(), 0)
