from django.contrib.auth.models import Group, Permission
from images.models import ImagesUser, Image
from images.custom_renderers import JPEGRenderer, PNGRenderer
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from images.serializers import *
import io
from PIL import Image as img


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

    @action(detail=False, methods=['GET'], name='Get picture',
            renderer_classes=(JPEGRenderer, PNGRenderer, JSONRenderer))
    def pics(self, request):
        queryset = Image.objects.get(creator=request.user, image_name=self.request.query_params.get('imagename'))
        size = self.request.query_params.get('size')

        if size not in (a.split('.')[1] for a in queryset.creator.get_all_permissions() if 'images' in a):
            return Response(data=JSONRenderer().render(
                data={'detail': f'Not permitted to get thumbnail size: {size}'}),
                status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        if size == 'full':  # return full-sized image before size validation
            new_img = img.open(queryset.image_fullres)
            x = io.BytesIO()
            new_img.save(x, new_img.format)
            return Response(x.getvalue())

        if int(size) > queryset.image_fullres.height:
            return Response(data=JSONRenderer().render(
                data={'detail': f'Image size lower than requested thumbnail size: {size}'}),
                status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

        # reopen because of that damn size validation...
        # https://code.djangoproject.com/ticket/13750 seems like it is not fixed after 13 years
        queryset.image_fullres.open()

        new_img = img.open(queryset.image_fullres)
        new_img.thumbnail(size=(int(new_img.height / (new_img.height / int(size))),
                                int(new_img.width / (new_img.width / int(size)))))

        x = io.BytesIO()
        new_img.save(x, new_img.format)

        return Response(x.getvalue())


class PermissionViewSet(ModelViewSet):
    """
    API endpoint that allows permissions to be viewed and created.
    """
    queryset = Permission.objects.filter(
        content_type_id='7')  # Shrink the permissions queryset just to image content type
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminUser]
