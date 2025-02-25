import os
import django

def pytest_configure(config):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'peers_backend.settings')
    django.setup()
