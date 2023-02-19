from django.contrib.auth.models import Group, Permission
from images.models import ImagesUser, Image
from images.custom_renderers import JPEGRenderer, PNGRenderer
from rest_framework.viewsets import ModelViewSet
# from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from images.serializers import *


class UserViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ImagesUser.objects.all().order_by('-date_joined')
    serializer_class = ImagesUserSerializer
    permission_classes = [IsAdminUser]


class GroupViewSet(ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]


class ImageViewSet(ModelViewSet):
    """
    API endpoint that allows images to be viewed or edited.
    """
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            queryset = Image.objects.all()
        else:
            queryset = Image.objects.filter(creator=self.request.user)

        return queryset


class PermissionViewSet(ModelViewSet):
    """
    API endpoint that allows permissions to be viewed and created.
    """
    queryset = Permission.objects.filter(
        content_type_id='7')  # Shrink the permissions queryset just to image content type
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminUser]
