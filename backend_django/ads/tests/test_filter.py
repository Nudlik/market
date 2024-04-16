from django.contrib.auth import get_user_model
from django.test import TestCase

from ads.filters import AdFilterSet
from ads.models import Ad


class TestAdFilterSet(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(email='1@1.ru', phone='+7123')
        self.user.set_password('1111')
        self.user.is_active = True
        self.user.save()

        self.ad1 = Ad.objects.create(title='title1', price=100, description='description1', author=self.user)
        self.ad2 = Ad.objects.create(title='title2', price=200, description='description2', author=self.user)
        self.ad3 = Ad.objects.create(title='title3', price=300, description='description3', author=self.user)

    def test_filter_title(self):
        ad_filter = AdFilterSet()
        qs = ad_filter.title_or_description_(Ad.objects.all(), '', '1')
        self.assertEqual(qs.last().title, 'title1')
