from django.test import RequestFactory, TestCase
from ..permissions import OnlyTutor, OnlyLearner, OnlyAnon, OnlyAdmin
from ..models import User
from django.contrib.auth.models import AnonymousUser

class TestOnlyTutorPermission(TestCase):
    def setUp(self):
        self.email = "email@test.com"
        self.password = "password"
        self.url = "/test/"
        self.factory = RequestFactory()

    def test_tutor_can_access(self):
        request = self.factory.get(self.url)
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            role=User.TUTOR
        )
        request.user = user
        permission = OnlyTutor()

        self.assertTrue(permission.has_permission(request, None))

    def test_admin_cannot_access(self):
        request = self.factory.get(self.url)
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            role=User.ADMIN
        )
        request.user = user
        permission = OnlyAnon()

        self.assertFalse(permission.has_permission(request, None))

    def test_learner_cannot_access(self):
        request = self.factory.get(self.url)
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            role=User.LEARNER
        )
        request.user = user
        permission = OnlyTutor()

        self.assertFalse(permission.has_permission(request, None))

    def test_anonymous_cannot_access(self):
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        permission = OnlyTutor()

        self.assertFalse(permission.has_permission(request, None))

class TestOnlyLearnerPermission(TestCase):
    def setUp(self):
        self.email = "email@test.com"
        self.password = "password"
        self.url = "/test/"
        self.factory = RequestFactory()

    def test_learner_can_access(self):
        request = self.factory.get(self.url)
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            role=User.LEARNER
        )
        request.user = user
        permission = OnlyLearner()

        self.assertTrue(permission.has_permission(request, None))

    def test_admin_cannot_access(self):
        request = self.factory.get(self.url)
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            role=User.ADMIN
        )
        request.user = user
        permission = OnlyAnon()

        self.assertFalse(permission.has_permission(request, None))

    def test_tutor_cannot_access(self):
        request = self.factory.get(self.url)
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            role=User.TUTOR
        )
        request.user = user
        permission = OnlyLearner()

        self.assertFalse(permission.has_permission(request, None))

    def test_anonymous_cannot_access(self):
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        permission = OnlyLearner()

        self.assertFalse(permission.has_permission(request, None))

class TestOnlyAnonPermission(TestCase):
    def setUp(self):
        self.email = "email@test.com"
        self.password = "password"
        self.url = "/test/"
        self.factory = RequestFactory()
    
    def test_anonymous_can_access(self):
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        permission = OnlyAnon()

        self.assertTrue(permission.has_permission(request, None))
    
    def test_admin_cannot_access(self):
        request = self.factory.get(self.url)
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            role=User.ADMIN
        )
        request.user = user
        permission = OnlyAnon()

        self.assertFalse(permission.has_permission(request, None))
        

    def test_learner_cannot_access(self):
        request = self.factory.get(self.url)
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            role=User.LEARNER
        )
        request.user = user
        permission = OnlyAnon()

        self.assertFalse(permission.has_permission(request, None))
      

    def test_tutor_cannot_access(self):
        request = self.factory.get(self.url)
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            role=User.TUTOR
        )
        request.user = user
        permission = OnlyAnon()

        self.assertFalse(permission.has_permission(request, None))
        
class TestOnlyLearnerPermission(TestCase):
    def setUp(self):
        self.email = "email@test.com"
        self.password = "password"
        self.url = "/test/"
        self.factory = RequestFactory()

    def test_admin_can_access(self):
        request = self.factory.get(self.url)
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            role=User.ADMIN
        )
        request.user = user
        permission = OnlyAdmin()

        self.assertTrue(permission.has_permission(request, None))

    def test_learner_cannot_access(self):
        request = self.factory.get(self.url)
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            role=User.LEARNER
        )
        request.user = user
        permission = OnlyAdmin()

        self.assertFalse(permission.has_permission(request, None))
        
    def test_tutor_cannot_access(self):
        request = self.factory.get(self.url)
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            role=User.TUTOR
        )
        request.user = user
        permission = OnlyAdmin()

        self.assertFalse(permission.has_permission(request, None))

    def test_anonymous_cannot_access(self):
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        permission = OnlyAdmin()

        self.assertFalse(permission.has_permission(request, None))