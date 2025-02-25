from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from account.models import User
from ..models import Tutor


class TutorModelTest(TestCase):
    email = 'testuser@example.com'
    password = 'testpass123'

    def setUp(self):
        self.user = User.objects.create(
            email='test1@test.com',
            password='test',
            role=User.LEARNER
        )

    def test_create_tutor_form(self):
        uid = self.user
        subject = "PPL"
        university = "Universitas Indonesia"
        pddikti = "https://pddikti.kemdikbud.go.id/data_mahasiswa/abcdef"
        ktp = SimpleUploadedFile('test_ktm.pdf', b'abcdef', content_type='application/pdf')
        transkrip = SimpleUploadedFile('test_transkrip.pdf', b'abcdef', content_type='application/pdf')
        ktm_person = SimpleUploadedFile('test_ktm_person.jpg', b'abcdef', content_type='image/jpeg')
        price_per_hour = 50000
        desc = "hello i'm a tutor"
        form = Tutor.objects.create(
            uid=self.user,
            subject=subject,
            university=university,
            pddikti=pddikti,
            ktp=ktp,
            transkrip=transkrip,
            ktm_person=ktm_person,
            price_per_hour=price_per_hour,
            desc=desc
        )

        self.assertEqual(form.uid, uid)
        self.assertEqual(form.subject, subject)
        self.assertEqual(form.university, university)
        self.assertEqual(form.pddikti, pddikti)
        self.assertEqual(form.ktp.name[-3:0], ktp.content_type[-3:0])
        self.assertEqual(form.transkrip.name[-3:0], transkrip.content_type[-3:0])
        self.assertIsNotNone(form.ktm_person)
        self.assertEqual(form.price_per_hour, price_per_hour)
        self.assertEqual(form.desc, desc)
