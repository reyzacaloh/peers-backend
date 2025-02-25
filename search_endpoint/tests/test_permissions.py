from django.test import RequestFactory, TestCase
from ..permissions import OnlyAuthenticated
from account.models import User
from django.contrib.auth.models import AnonymousUser
class TestOnlyTutorPermission(TestCase):
    def setUp(self):
        self.email = "email@test.com"
        self.password = "password"
        self.url = "/test/"
        self.factory = RequestFactory()

    def test_authenticated_can_access(self):
        request = self.factory.get(self.url)
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            role=User.TUTOR
        )
        request.user = user
        permission = OnlyAuthenticated()
        self.assertTrue(permission.has_permission(request, None))

    def test_unauthenticated_cannot_access(self):
        request = self.factory.get(self.url)
        user = AnonymousUser()
        request.user = user
        permission = OnlyAuthenticated()
        self.assertFalse(permission.has_permission(request, None))
