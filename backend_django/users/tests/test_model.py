from django.contrib.auth import get_user_model
from django.test import TestCase


class UserManagerTest(TestCase):

    def setUp(self):
        self.user_manager = get_user_model()
        self.email = '1@1.ru'
        self.password = '1111'
        self.extra_fields = {'is_staff': True, 'is_superuser': True, 'role': 'admin'}

    def test_create_superuser(self):
        user = self.user_manager.objects.create_superuser(self.email, self.password, **self.extra_fields)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.role, 'admin')
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))

    def test_create_superuser_without_staff(self):
        self.extra_fields = {'is_staff': False, 'is_superuser': True, 'role': 'admin'}
        with self.assertRaises(ValueError):
            self.user_manager.objects.create_superuser(self.email, self.password, **self.extra_fields)

    def test_create_superuser_without_superuser(self):
        self.extra_fields = {'is_staff': True, 'is_superuser': False, 'role': 'admin'}
        with self.assertRaises(ValueError):
            self.user_manager.objects.create_superuser(self.email, self.password, **self.extra_fields)

    def test_create_superuser_without_role(self):
        self.extra_fields = {'is_staff': True, 'is_superuser': True, 'role': ''}
        with self.assertRaises(ValueError):
            self.user_manager.objects.create_superuser(self.email, self.password, **self.extra_fields)

    def test_create_user_without_email(self):
        self.extra_fields = {'is_staff': True, 'is_superuser': True, 'role': 'admin'}
        self.email = None
        with self.assertRaises(ValueError):
            self.user_manager.objects.create_user(email=self.email, password=self.password, **self.extra_fields)

    def test_property_is_admin(self):
        user = self.user_manager.objects.create_user(email=self.email, password=self.password, **self.extra_fields)
        self.assertTrue(user.is_admin)

    def test_property_is_user(self):
        self.extra_fields = {}
        user = self.user_manager.objects.create_user(email=self.email, password=self.password, **self.extra_fields)
        self.assertTrue(user.is_user)

    def test_has_module_perms(self):
        user = self.user_manager.objects.create_user(email=self.email, password=self.password, **self.extra_fields)
        self.assertTrue(user.has_module_perms('users'))

    def test_has_perm(self):
        user = self.user_manager.objects.create_user(email=self.email, password=self.password, **self.extra_fields)
        self.assertTrue(user.has_perm('users.add_user'))
