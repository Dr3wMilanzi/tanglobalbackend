from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser, CompanyContactDetails

class CreateUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_individual_user(self):
        # Create an individual user
        data = {'email': 'individual@example.com', 'password': 'password123', 'is_individual': True}
        response = self.client.post('api/v1/auth/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_create_business_user(self):
        # Create a business user
        data = {'email': 'business@example.com', 'password': 'password123', 'is_cargo_owner': True}
        response = self.client.post('api/v1/auth/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CompanyContactDetails.objects.count(), 1)
        company_details = CompanyContactDetails.objects.first()
        self.assertEqual(company_details.user.email, 'business@example.com')
        self.assertEqual(company_details.company_name, 'Your Company Name')

    def test_create_invalid_user(self):
        # Try to create a user with missing required fields
        data = {'password': 'password123'}
        response = self.client.post('api/v1/auth/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 0)
        self.assertEqual(CompanyContactDetails.objects.count(), 0)
