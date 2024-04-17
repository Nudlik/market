from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from ads.models import Ad


class AdViewSetTestCase(TestCase):

    def setUp(self):
        self.total_users = 3

        self.user = get_user_model().objects.create(email='1@1.ru', phone='+7123')
        self.user.set_password('1111')
        self.user.save()

        self.user2 = get_user_model().objects.create(email='2@2.ru', phone='+7123')
        self.user2.set_password('1111')
        self.user2.save()

        self.admin = get_user_model().objects.create(email='admin@admin.ru', phone='+7123')
        self.admin.set_password('1111')
        self.admin.is_staff = True
        self.admin.save()

        self.total_ads = 3
        self.ad1 = Ad.objects.create(title='title1', price=100, description='description1', author=self.user)
        self.ad2 = Ad.objects.create(title='title2', price=200, description='description2', author=self.user2)
        self.ad3 = Ad.objects.create(title='title3', price=300, description='description3', author=self.admin)

    def test_ad_create(self):
        data = {
            'title': 'new ad',
            'price': 100,
            'description': 'new ad description',
        }
        self.client.force_login(self.user)
        url = reverse('ads-list')
        response = self.client.post(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ad.objects.count(), self.total_ads + 1)
        self.assertEqual(Ad.objects.last().author, self.user)

    def test_ad_list(self):
        url = reverse('ads-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), self.total_ads)

    def test_ad_me(self):
        self.client.force_login(self.user)
        url = reverse('ads-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_ad_delete(self):
        self.client.force_login(self.user)
        url = reverse('ads-detail', kwargs={'pk': self.ad1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ad.objects.count(), self.total_ads - 1)

    def test_ad_delete_not_author(self):
        self.client.force_login(self.user2)
        url = reverse('ads-detail', kwargs={'pk': self.ad1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Ad.objects.count(), self.total_ads)

    def test_ad_delete_admin(self):
        self.client.force_login(self.admin)
        url = reverse('ads-detail', kwargs={'pk': self.ad1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ad.objects.count(), self.total_ads - 1)

    def test_ad_update(self):
        self.client.force_login(self.user)
        data = {
            'title': 'new ad',
            'price': 100,
            'description': 'new ad description',
        }
        url = reverse('ads-detail', kwargs={'pk': self.ad1.pk})
        response = self.client.patch(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_ad = Ad.objects.get(pk=self.ad1.pk)
        self.assertEqual(updated_ad.title, 'new ad')
        self.assertEqual(updated_ad.price, 100)
        self.assertEqual(updated_ad.description, 'new ad description')

    def test_ad_update_not_author(self):
        self.client.force_login(self.user2)
        data = {
            'title': 'new ad',
            'price': 0,
            'description': 'new ad description',
        }
        url = reverse('ads-detail', kwargs={'pk': self.ad1.pk})
        response = self.client.patch(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        updated_ad = Ad.objects.get(pk=self.ad1.pk)
        self.assertNotEqual(updated_ad.title, 'new ad')
        self.assertNotEqual(updated_ad.price, 0)
        self.assertNotEqual(updated_ad.description, 'new ad description')
