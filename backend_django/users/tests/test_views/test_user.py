from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class UserViewSetTestCase(TestCase):

    def setUp(self):
        self.total_users = 2

        self.user = get_user_model().objects.create(email='1@1.ru', phone='+7123')
        self.user.set_password('1111')
        self.user.is_active = True
        self.user.save()

        self.admin = get_user_model().objects.create(email='admin@admin.ru', phone='+7123')
        self.admin.set_password('1111')
        self.admin.is_active = True
        self.admin.is_staff = True
        self.admin.save()

    def test_create_user(self):
        data = {
            'email': 'test2@example.com',
            'password': 'testpassword',
            'phone': '+71234567890'
        }
        url = reverse('users-list')
        response = self.client.post(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), self.total_users + 1)

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

    def test_update_user_bad(self):
        user2 = get_user_model().objects.create(email='2@2.ru', phone='+7123')
        user2.set_password('1111')
        user2.is_active = True
        user2.save()
        data = {
            'first_name': 'Your_first_name',
        }
        url = reverse('users-detail', args=[self.user.id])
        self.client.force_login(user2)
        response = self.client.patch(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.user.first_name, '')

    def test_update_user_admin(self):
        data = {
            'first_name': 'Your_first_name',
        }
        url = reverse('users-detail', args=[self.user.id])
        self.client.force_login(self.admin)
        response = self.client.patch(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['first_name'], 'Your_first_name')
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Your_first_name')

    def test_delete_user(self):
        data = {
            'email': self.user.email,
            'phone': self.user.phone,
        }
        url = reverse('users-me')
        self.client.force_login(self.user)
        response = self.client.delete(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(get_user_model().objects.count(), self.total_users - 1)

    def test_views_user(self):
        url = reverse('users-detail', args=[self.user.id])
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
