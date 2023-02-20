from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def content_file_name(instance, filename):
    return '/'.join([instance.creator.username, filename])


def nowplustimedelta():
    return timezone.now() + timezone.timedelta(seconds=300)


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
    image_fullres = models.ImageField('Image', default=None, upload_to=content_file_name)
    image_name = models.CharField(max_length=50, default=None)
    binary = models.BinaryField(default=b'XD')
    creator = models.ForeignKey(ImagesUser, on_delete=models.CASCADE)
