from django.contrib.auth import get_user_model
from django.test import TestCase

from ads.models import Comment, Ad


class TestCommentModel(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(email='1@1.ru', phone='+7123')
        self.user.set_password('1111')
        self.user.is_active = True
        self.user.save()

        self.ad1 = Ad.objects.create(title='title1', price=100, description='description1', author=self.user)
        self.comment1 = Comment.objects.create(text='text1', author=self.user, ad=self.ad1)

    def test_str(self):
        self.assertEqual(str(self.comment1), 'title1 - 1@1.ru: text1')
        self.assertEqual(str(self.comment1), f'{self.ad1} - {self.user}: {self.comment1.text[:20]}')
