from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase

from account.models import User
from model_bakery import baker

from ..models import Tutor
from ..serializers import TutorSerializer


class TutorSerializerTestCase(APITestCase):
    def setUp(self):
        self.tutor = baker.make(Tutor)
        self.validated_data = {
            'uid': self.tutor.uid,
            'subject': 'Mathematics',
            'university': 'University of California',
            'pddikti': '12345',
            'ktm_person': SimpleUploadedFile("file.txt", b"file_content"),
            'ktp': SimpleUploadedFile("file.txt", b"file_content"),
            'transkrip': SimpleUploadedFile("file.txt", b"file_content"),
            'is_verified': True,
            'is_accepted': True,
            'is_submitted': True
        }

    def test_valid_serializer(self):
        serializer = TutorSerializer(data=self.validated_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer_missing_required_field(self):
        self.validated_data.pop('ktm_person')
        serializer = TutorSerializer(data=self.validated_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'ktm_person'})
