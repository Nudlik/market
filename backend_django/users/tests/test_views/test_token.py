from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class TokenTestCase(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create(email='1@1.ru', phone='+7123')
        self.user.set_password('1111')
        self.user.is_active = True
        self.user.save()

    def test_user_create(self):
        data = {
            'email': '2@2.ru',
            'password': '1111',
            'phone': '+7123',
        }
        url = reverse('users-list')
        self.client.post(url, data, 'application/json')
        self.assertEqual(get_user_model().objects.last().email, data['email'])
        self.assertEqual(get_user_model().objects.all().count(), 2)

    def test_user_token_login(self):
        # token
        data = {
            'email': self.user.email,
            'password': '1111'
        }
        url = reverse('token-create')
        response = self.client.post(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        access_token = response.data['access']

        # refresh
        url = reverse('token-refresh')
        refresh = response.data['refresh']
        response = self.client.post(url, {'refresh': refresh}, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertNotEquals(access_token, response.data['access'])
