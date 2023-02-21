from uuid import uuid4

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from images.models import ImagesUser, Image
from django.contrib.auth.models import Group, Permission
from PIL import Image as Img
from io import BytesIO


def mock_test_image(fmt='jpeg', size=(1000, 1000)):
    img_bytes = BytesIO()
    img = Img.new('RGB', size)
    img.save(img_bytes, fmt)
    img_bytes.seek(0)
    return SimpleUploadedFile(f'test.{fmt}', img_bytes.getvalue())


class ImagesUserCreateTestCase(APITestCase):
    #
    def setUp(self) -> None:
        self.user = ImagesUser.objects.create_user('john', 'john@hexocean.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.userdata = {'username': 'testuser', 'email': 'testuser@hexocean.com', 'password': 'strongerpassword#1!'}
        self.groupdata = {'name': 'testgroup'}
        self.permissiondata = {'codename': '100', 'name': 'Can get 100px in height image'}

    def test_cant_create_imagesuser(self):
        response = self.client.post(reverse('imagesuser-list'), self.userdata)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cant_create_group(self):
        response = self.client.post(reverse('group-list'), self.groupdata)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cant_create_permission(self):
        response = self.client.post(reverse('permission-list'), self.permissiondata)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ImagesUserReadTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = ImagesUser.objects.create_user('john', 'john@hexocean.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.custom_perm = Permission.objects.create(codename=300,
                                                     name='Can get 300px in height images',
                                                     content_type_id=7)

        # create default tiers
        self.basic = Group.objects.get_or_create(name='Basic')
        self.basic[0].permissions.add(
            Permission.objects.get(codename='200'),
            Permission.objects.get(codename='add_image'),
            Permission.objects.get(codename='delete_image'),
            Permission.objects.get(codename='view_image')
        )

        self.premium = Group.objects.get_or_create(name='Premium')
        self.premium[0].permissions.add(
            Permission.objects.get(codename='200'),
            Permission.objects.get(codename='400'),
            Permission.objects.get(codename='add_image'),
            Permission.objects.get(codename='delete_image'),
            Permission.objects.get(codename='view_image')
        )

        self.enterprise = Group.objects.get_or_create(name='Enterprise')
        self.enterprise[0].permissions.add(
            Permission.objects.get(codename='200'),
            Permission.objects.get(codename='400'),
            Permission.objects.get(codename='full'),
            Permission.objects.get(codename='expiring_links'),
            Permission.objects.get(codename='add_image'),
            Permission.objects.get(codename='delete_image'),
            Permission.objects.get(codename='view_image')
        )

        # create custom tier
        self.custom = Group.objects.get_or_create(name='Custom')
        self.custom[0].permissions.add(
            Permission.objects.get(codename='200'),
            Permission.objects.get(codename='300'),
            Permission.objects.get(codename='400'),
            Permission.objects.get(codename='full'),
            Permission.objects.get(codename='expiring_links'),
            Permission.objects.get(codename='add_image'),
            Permission.objects.get(codename='delete_image'),
            Permission.objects.get(codename='view_image')
        )

        x = mock_test_image()
        self.image = Image.objects.create(image_name=f"{uuid4()}.jpeg", image_fullres=x, binary=x.read(),
                                          creator=self.user)

    def test_cant_read_imagesuser(self):
        response = self.client.get(reverse('imagesuser-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cant_read_group(self):
        response = self.client.get(reverse('group-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cant_read_permission(self):
        response = self.client.get(reverse('permission-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cant_read_images(self):
        response = self.client.get(reverse('image-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg='No tier has access')

    def test_can_read_images_basic(self):
        self.user.groups.add(self.basic[0])  # assign basic tier

        response = self.client.get(reverse('image-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg='Basic tier has no access')
        self.assertEqual(len(response.data['results'][0]['pic_urls'].keys()), 1)

    def test_can_read_images_premium(self):
        self.user.groups.add(self.premium[0])  # assign premium tier

        response = self.client.get(reverse('image-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg='Premium tier has no access')
        self.assertEqual(len(response.data['results'][0]['pic_urls'].keys()), 2)

    def test_can_read_images_enterprise(self):
        self.user.groups.add(self.enterprise[0])  # assign enterprise tier

        response = self.client.get(reverse('image-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg='Enterprise tier has no access')
        self.assertEqual(len(response.data['results'][0]['pic_urls'].keys()), 4)

    def test_can_read_images_custom(self):
        self.user.groups.add(self.custom[0])  # assign custom tier

        response = self.client.get(reverse('image-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg='Enterprise tier has no access')
        self.assertEqual(len(response.data['results'][0]['pic_urls'].keys()), 5)

    def test_can_read_images_expiring_link(self):
        self.user.groups.add(self.enterprise[0])  # assign enterprise tier
        # had to parse it by hand, get with params didnt work :/
        url = f"{reverse('image-generate-temp-url')}?imagename={self.image.image_name}&timeout=30000"
        response2 = self.client.get(url)
        response3 = self.client.get(response2.data['link'])
        self.assertEqual(response3.status_code, status.HTTP_301_MOVED_PERMANENTLY)
