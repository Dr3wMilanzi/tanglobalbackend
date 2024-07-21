from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import VehicleType, Vehicle, VehicleImage

User = get_user_model()

class VehicleTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.vehicle_type = VehicleType.objects.create(name='Sedan')

    def test_create_vehicle_with_images(self):
        url = reverse('vehicle-list')
        data = {
            'vehicle_type': self.vehicle_type.id,
            'model': 'Model S',
            'registration_number': 'ABC123',
            'capacity': 5,
            'created_by': self.user.id,
            'image_files': [
                self._create_test_image(),
                self._create_test_image()
            ]
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vehicle.objects.count(), 1)
        self.assertEqual(VehicleImage.objects.count(), 2)
        vehicle = Vehicle.objects.get()
        self.assertEqual(vehicle.images.count(), 2)

    def _create_test_image(self):
        from io import BytesIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        from PIL import Image

        file = BytesIO()
        image = Image.new('RGB', (100, 100))
        image.save(file, 'jpeg')
        file.seek(0)
        return SimpleUploadedFile('test_image.jpg', file.read(), content_type='image/jpeg')
