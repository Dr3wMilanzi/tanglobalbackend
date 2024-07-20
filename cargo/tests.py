# tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Cargo, CargoType
from .serializers import CargoSerializer

class CargoModelTest(TestCase):
    def setUp(self):
        self.cargo_type = CargoType.objects.create(name="Electronics")
        self.cargo = Cargo.objects.create(
            cargo='Laptop',
            weight=5.5,
            cargo_type=self.cargo_type,
            weight_unit='kg',
            length=30.0,
            width=20.0,
            height=5.0,
            fragile=True,
            temperature_sensitive=False,
            origin='Warehouse A',
            destination='Warehouse B',
            receiver_name='John Doe',
            receiver_contact='1234567890',
            slug='laptop-slug'  # Ensure the slug is unique and set
        )

    def test_cargo_creation(self):
        self.assertEqual(self.cargo.cargo, "Laptop")
        self.assertEqual(self.cargo.weight, 5.5)
        self.assertTrue(self.cargo.fragile)
        self.assertEqual(self.cargo.slug, 'laptop-slug')

    def test_cargo_str_representation(self):
        self.assertEqual(str(self.cargo), "Laptop - 5.5kg")

class CargoViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cargo_type = CargoType.objects.create(name="Electronics")
        self.cargo = Cargo.objects.create(
            cargo='Laptop',
            weight=5.5,
            cargo_type=self.cargo_type,
            weight_unit='kg',
            length=30.0,
            width=20.0,
            height=5.0,
            fragile=True,
            temperature_sensitive=False,
            origin='Warehouse A',
            destination='Warehouse B',
            receiver_name='John Doe',
            receiver_contact='1234567890',
            slug='laptop-slug'
        )
        self.cargo_url = reverse('cargo-detail', kwargs={'slug': self.cargo.slug})

    def test_get_single_cargo(self):
        response = self.client.get(self.cargo_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.cargo.slug)

    def test_create_cargo(self):
        cargo_data = {
            'cargo': 'Smartphone',
            'weight': 0.3,
            'cargo_type': self.cargo_type.id,
            'weight_unit': 'kg',
            'length': 10.0,
            'width': 5.0,
            'height': 0.8,
            'fragile': True,
            'temperature_sensitive': True,
            'origin': 'Factory B',
            'destination': 'Warehouse C',
            'receiver_name': 'Alice Smith',
            'receiver_contact': '9876543210',
            'slug': 'smartphone-slug'
        }
        response = self.client.post(reverse('cargo-list'), cargo_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cargo.objects.count(), 2)

    def test_update_cargo(self):
        update_data = {'weight': 6.0}
        response = self.client.patch(self.cargo_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cargo.refresh_from_db()
        self.assertEqual(self.cargo.weight, 6.0)

    def test_delete_cargo(self):
        response = self.client.delete(self.cargo_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cargo.objects.count(), 0)