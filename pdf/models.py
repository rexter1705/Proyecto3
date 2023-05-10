from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class UploadFile(models.Model):
    file = models.FileField(upload_to='media')
    text = models.TextField(blank=True, null=True)


    