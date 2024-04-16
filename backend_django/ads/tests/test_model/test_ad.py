from django.contrib.auth import get_user_model
from django.test import TestCase

from ads.models import Ad


class TestAdModel(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(email='1@1.ru', phone='+7123')
        self.user.set_password('1111')
        self.user.is_active = True
        self.user.save()

        self.ad1 = Ad.objects.create(title='title1', price=100, description='description1', author=self.user)

    def test_str(self):
        self.assertEqual(str(self.ad1), 'title1')
