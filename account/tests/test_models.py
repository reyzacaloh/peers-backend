from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from ..managers import CustomUserManager


class UserModelTest(TestCase):
    email = 'testuser@example.com'
    password = 'testpass123'

    def setUp(self):
        self.user_manager = CustomUserManager()
        self.User = get_user_model()

    def test_create_user(self):
        user = self.User.objects.create_user(
            email=self.email,
            password=self.password
        )

        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_admin)

    def test_create_superuser(self):
        user = self.User.objects.create_superuser(
            email=self.email,
            password=self.password
        )

        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_admin)

    def test_str(self):
        user = self.User.objects.create_user(email=self.email, password="halo")
        self.assertEqual(str(user), self.email)

    

    def test_required_fields(self):
        required_fields = self.User.REQUIRED_FIELDS
        self.assertEqual(required_fields, [])

    def test_username_field(self):
        username_field = self.User.USERNAME_FIELD
        self.assertEqual(username_field, 'email')

    def test_create_user_with_extra_fields(self):
        first_name = 'Test'
        last_name = 'User'
        date_of_birth = '1990-01-01'
        profile_picture = SimpleUploadedFile('test_image.jpg', b'abcdef', content_type='image/jpeg')
        user = self.User.objects.create_user(
            email=self.email,
            password=self.password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            profile_picture=profile_picture,
        )

        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.date_of_birth, date_of_birth)
        self.assertIsNotNone(user.profile_picture)