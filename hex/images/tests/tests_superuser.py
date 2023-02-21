from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from images.models import ImagesUser, Image


class ImagesSuperUserCreateTestCase(APITestCase):
    def setUp(self) -> None:
        self.superuser = ImagesUser.objects.create_superuser('john', 'john@hexocean.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.userdata = {'username': 'testuser', 'email': 'testuser@hexocean.com', 'password': 'strongerpassword#1!'}
        self.groupdata = {'name': 'testgroup'}
        self.permissiondata = {'codename': '100', 'name': 'Can get 200px in height image'}

    def test_can_create_imagesuser(self):
        response = self.client.post(reverse('imagesuser-list'), self.userdata, 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_create_group(self):
        response = self.client.post(reverse('group-list'), self.groupdata, 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_create_permission(self):
        response = self.client.post(reverse('permission-list'), self.permissiondata, 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ImagesSuperUserReadTestCase(APITestCase):
    def setUp(self) -> None:
        self.superuser = ImagesUser.objects.create_superuser('john', 'john@hexocean.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.data = {'username': 'testuser', 'email': 'testuser@hexocean.com', 'password': 'strongerpassword#1!'}

    def test_can_read_imagesuser(self):
        response = self.client.get(reverse('imagesuser-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_group(self):
        response = self.client.get(reverse('group-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_permission(self):
        response = self.client.get(reverse('permission-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
