from django.contrib.auth.models import Group, Permission
from images.models import ImagesUser, Image
from images.custom_renderers import JPEGRenderer, PNGRenderer
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from images.permissions import HasImagePermission, ReadOnly
from rest_framework import status
from images.serializers import *
import io
from PIL import Image as Img

from django.core import signing


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
    permission_classes = [HasImagePermission or IsAdminUser]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            queryset = Image.objects.all()
        else:
            queryset = Image.objects.filter(creator=self.request.user)

        return queryset

    # making it world readable because otherwise it's pointless imo
    # all creator permissions are applied, so even anonymous user will not get "extra" sizes
    @action(detail=False,
            methods=['GET'],
            name='Get picture',
            renderer_classes=(JPEGRenderer, PNGRenderer, JSONRenderer),
            permission_classes=[HasImagePermission | ReadOnly])
    def pics(self, attrs):
        """API parametrized endpoint to get images"""
        if 'temp' in self.request.query_params and 'timeout' in self.request.query_params:
            try:
                signed_data = self.request.query_params.get('temp')
                timeout = self.request.query_params.get('timeout')
                data = signing.loads(signed_data, max_age=int(timeout))
                data_id, data_timeout = data.split(',')
                image = Image.objects.get(id=data_id)
            except signing.SignatureExpired:
                return Response(JSONRenderer().render(data={'detail': f'Link expired'}),
                                status=status.HTTP_400_BAD_REQUEST,
                                content_type='application/json')

            except signing.BadSignature:
                return Response(JSONRenderer().render(data={'detail': f'Invalid url'}),
                                status=status.HTTP_400_BAD_REQUEST,
                                content_type='application/json')

            new_img = Img.open(image.image_fullres)
            x = io.BytesIO()
            new_img.save(x, new_img.format)
            return Response(x.getvalue())

        queryset = Image.objects.get(image_name=self.request.query_params.get('imagename'))
        size = self.request.query_params.get('size')

        if size not in (a.split('.')[1] for a in queryset.creator.get_all_permissions() if 'images' in a):
            return Response(data=JSONRenderer().render(
                data={'detail': f'Not permitted to get thumbnail size: {size}'}),
                status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        if size == 'full':  # return full-sized image before size validation
            new_img = Img.open(queryset.image_fullres)
            x = io.BytesIO()
            new_img.save(x, new_img.format)
            return Response(x.getvalue())

        if int(size) > queryset.image_fullres.height:  # resizing image based on height, so not checking width
            return Response(data=JSONRenderer().render(
                data={'detail': f'Image size lower than requested thumbnail size: {size}'}),
                status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

        # reopen because of size validation...
        # https://code.djangoproject.com/ticket/13750 seems like it is not fixed after 13 years
        queryset.image_fullres.open()

        new_img = Img.open(queryset.image_fullres)
        new_img.thumbnail(size=(int(new_img.height / (new_img.height / int(size))),
                                int(new_img.width / (new_img.width / int(size)))))

        x = io.BytesIO()
        new_img.save(x, new_img.format)

        return Response(x.getvalue())

    @action(detail=False,
            methods=['GET'],
            name='Get temporary link',
            permission_classes=(IsAuthenticated, ))
    def generate_temp_url(self, attrs):
        """API parametrized endpoint to get temporary link"""
        if not self.request.query_params.get('timeout').isdigit():
            return Response(data={'detail': f'Invalid timeout format'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not api_settings.user_settings.get('MIN_TEMP_SECONDS') <= int(self.request.query_params.get(
                'timeout')) <= api_settings.user_settings.get('MAX_TEMP_SECONDS'):
            return Response(data={'detail': f'Timeout exceeds (300..30000) range'},
                            status=status.HTTP_400_BAD_REQUEST)
        signed = signing.dumps(f'{Image.objects.get(image_name=self.request.query_params.get("imagename")).id},'
                               f'{self.request.query_params.get("timeout")}')

        return Response(data={'detail': f'Link created',
                              'link': f'http://{attrs.get_host()}/images/pics?temp={signed}&timeout={self.request.query_params.get("timeout")}'},
                        status=status.HTTP_201_CREATED)


class PermissionViewSet(ModelViewSet):
    """
    API endpoint that allows permissions to be viewed and created.
    """
    # Shrink the permissions queryset just to image content type
    queryset = Permission.objects.filter(content_type_id='7')
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminUser]
