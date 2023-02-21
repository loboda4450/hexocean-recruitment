from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from images.models import ImagesUser, Image


class ImagesUserCreateTestCase(APITestCase):
    #
    def setUp(self) -> None:
        self.user = ImagesUser.objects.create_user('john', 'john@hexocean.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.userdata = {'username': 'testuser', 'email': 'testuser@hexocean.com', 'password': 'strongerpassword#1!'}
        self.groupdata = {'name': 'testgroup'}
        self.permissiondata = {'codename': '100', 'name': 'Can get 200px in height image'}

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

    def test_cant_read_imagesuser(self):
        response = self.client.get(reverse('imagesuser-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cant_read_group(self):
        response = self.client.get(reverse('group-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cant_read_permission(self):
        response = self.client.get(reverse('permission-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
