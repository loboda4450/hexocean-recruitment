from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.conf import settings


class ImagesUser(User):
    class Meta:
        proxy = True
        ordering = ('-date_joined',)
        permissions = (('200', 'Can get 200px in height image'),
                       ('400', 'Can get 400px in height image'),
                       ('full', 'Can get image in original resolution'),
                       ('expiring_links', 'Can get expiring link'))


class Image(models.Model):
    date_posted = models.DateTimeField('Date posted', default=timezone.now)
    image_fullres = models.ImageField('Image', default=None, upload_to='pics/')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
