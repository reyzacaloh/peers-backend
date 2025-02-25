from django.test import TestCase
from django.conf import settings
from peers_backend.fileutils import getFileS3URL

class TestFileUtilsFunctions(TestCase):
    
    def test_getFileS3URL(self):
        # Test case 1
        key = 'my-file.txt'
        expected_url = f"{settings.S3_HOST}{key}"
        self.assertEqual(getFileS3URL(key), expected_url)

        # Test case 2
        key = 'folder1/my-file.png'
        expected_url = f"{settings.S3_HOST}{key}"
        self.assertEqual(getFileS3URL(key), expected_url)
