
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import UpdateType, Update

class UpdateTypeAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.update_type = UpdateType.objects.create(name='Weekly Update')

    def test_create_update_type(self):
        url = reverse('updatetype-list')
        data = {'name': 'Monthly Update'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UpdateType.objects.count(), 2)

    def test_update_type_details(self):
        url = reverse('updatetype-detail', kwargs={'pk': self.update_type.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Weekly Update')

class UpdateAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.update_type = UpdateType.objects.create(name='Daily Update')
        self.update = Update.objects.create(name='System Maintenance', update_type=self.update_type, created_by=self.user)

    def test_list_updates(self):
        url = reverse('update-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_approve_update(self):
        url = reverse('approve-update', kwargs={'slug': self.update.slug})
        response = self.client.patch(url, {})
        self.update.refresh_from_db()
        self.assertTrue(self.update.is_approved)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
