# tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Cargo
from .serializers import CargoSerializer

class CargoModelTest(TestCase):
    def setUp(self):
        self.cargo = Cargo.objects.create(
            name="Test Cargo",
            description="This is a test cargo",
            weight=100.5
        )

    def test_cargo_creation(self):
        self.assertEqual(self.cargo.name, "Test Cargo")
        self.assertEqual(self.cargo.description, "This is a test cargo")
        self.assertEqual(self.cargo.weight, 100.5)

    def test_cargo_str_representation(self):
        self.assertEqual(str(self.cargo), "Test Cargo")

class CargoSerializerTest(TestCase):
    def setUp(self):
        self.cargo_attributes = {
            'name': 'Test Cargo',
            'description': 'This is a test cargo',
            'weight': 100.5
        }
        self.cargo = Cargo.objects.create(**self.cargo_attributes)
        self.serializer = CargoSerializer(instance=self.cargo)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'name', 'description', 'weight']))

    def test_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.cargo_attributes['name'])
        self.assertEqual(data['description'], self.cargo_attributes['description'])
        self.assertEqual(data['weight'], self.cargo_attributes['weight'])

class CargoViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cargo_data = {
            'name': 'Test Cargo',
            'description': 'This is a test cargo',
            'weight': 100.5
        }
        self.cargo = Cargo.objects.create(**self.cargo_data)
        self.cargo_url = reverse('cargo-detail', kwargs={'pk': self.cargo.pk})

    def test_get_all_cargoes(self):
        response = self.client.get(reverse('cargo-list'))
        cargoes = Cargo.objects.all()
        serializer = CargoSerializer(cargoes, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_cargo(self):
        response = self.client.get(self.cargo_url)
        cargo = Cargo.objects.get(pk=self.cargo.pk)
        serializer = CargoSerializer(cargo)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_cargo(self):
        response = self.client.post(reverse('cargo-list'), self.cargo_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_cargo(self):
        updated_cargo_data = {
            'name': 'Updated Cargo',
            'description': 'This is an updated test cargo',
            'weight': 150.75
        }
        response = self.client.put(self.cargo_url, updated_cargo_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_cargo(self):
        response = self.client.delete(self.cargo_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)