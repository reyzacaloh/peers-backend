from django.conf import settings

def getFileS3URL(key: str) -> str:
    return "{S3HOST}{KEY}".format(S3HOST=settings.S3_HOST, KEY=key)