from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from ads.models import Ad, Comment


class CommentViewSetTestCase(TestCase):

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

        self.total_comments = 3
        self.comment1 = Comment.objects.create(text='text1', author=self.user, ad=self.ad1)
        self.comment2 = Comment.objects.create(text='text2', author=self.user2, ad=self.ad2)
        self.comment3 = Comment.objects.create(text='text3', author=self.admin, ad=self.ad3)

    def test_list(self):
        self.client.force_login(self.user)
        url = reverse('comments-list', kwargs={'ad_pk': self.ad1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_create(self):
        self.client.force_login(self.user)
        url = reverse('comments-list', kwargs={'ad_pk': self.ad1.pk})
        data = {
            'text': 'text4',
        }
        response = self.client.post(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), self.total_comments + 1)

    def test_update(self):
        self.client.force_login(self.user)
        url = reverse('comments-detail', kwargs={'ad_pk': self.ad1.pk, 'pk': self.comment1.pk})
        data = {
            'text': 'text4',
        }
        response = self.client.patch(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.get(pk=self.comment1.pk).text, 'text4')

    def test_update_bad(self):
        self.client.force_login(self.user2)
        url = reverse('comments-detail', kwargs={'ad_pk': self.ad1.pk, 'pk': self.comment1.pk})
        data = {
            'text': 'text4',
        }
        response = self.client.patch(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_admin(self):
        self.client.force_login(self.admin)
        url = reverse('comments-detail', kwargs={'ad_pk': self.ad1.pk, 'pk': self.comment1.pk})
        data = {
            'text': 'text4',
        }
        response = self.client.patch(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.get(pk=self.comment1.pk).text, 'text4')

    def test_destroy(self):
        self.client.force_login(self.user)
        url = reverse('comments-detail', kwargs={'ad_pk': self.ad1.pk, 'pk': self.comment1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), self.total_comments - 1)

    def test_destroy_bad(self):
        self.client.force_login(self.user2)
        url = reverse('comments-detail', kwargs={'ad_pk': self.ad1.pk, 'pk': self.comment1.pk})
        self.assertEqual(self.ad1.author, self.user)
        self.assertEqual(self.comment1.author, self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_admin(self):
        self.client.force_login(self.admin)
        url = reverse('comments-detail', kwargs={'ad_pk': self.ad1.pk, 'pk': self.comment1.pk})
        self.assertEqual(self.ad1.author, self.user)
        self.assertEqual(self.comment1.author, self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), self.total_comments - 1)
