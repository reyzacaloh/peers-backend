from django.test import TestCase
from django.contrib.auth import get_user_model
from ..managers import CustomUserManager


class CustomUserManagerTest(TestCase):
    def setUp(self):
        self.user_manager = CustomUserManager()
        self.User = get_user_model()

    def test_create_user(self):
        email = 'testuser@example.com'
        password = 'testpass123'
        user = self.User.objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        email = 'testsuperuser@example.com'
        password = 'testpass123'
        user = self.User.objects.create_superuser(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_with_no_email(self):
        password = 'testpass123'

        with self.assertRaises(ValueError):
            self.user_manager.create_user(
                email=None,
                password=password
            )

    def test_create_user_with_no_password(self):
        email = 'testuser@example.com'

        with self.assertRaises(ValueError):
            self.user_manager.create_user(
                email=email,
                password=None
            )

    def test_create_superuser_with_wrong_role(self):
        email = 'testsuperuser@example.com'
        password = 'testpass123'

        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email=email,
                password=password,
                role=2
            )

    def test_create_user_using_user_object(self):
        email = 'testuser@example.com'
        password = 'testpass123'
        user = self.User(
            email=email,
            password=password
        )
        user.set_password(password)

        user.save()

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)