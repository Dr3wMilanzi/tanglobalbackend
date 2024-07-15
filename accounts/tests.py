from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Company, Invitation, CompanyMember
import uuid

User = get_user_model()

class UserOnboardingTests(APITestCase):
    def test_user_registration(self):
        url = reverse('onboarding-list')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'full_name': 'Test User',
            'phone_number': '1234567890',
            'address': '123 Test St',
            'is_individual': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@example.com')

    def test_company_registration(self):
        url = reverse('onboarding-list')
        data = {
            'email': 'testcompany@example.com',
            'password': 'testpassword123',
            'full_name': 'Test Company',
            'phone_number': '1234567890',
            'address': '123 Company St',
            'is_company': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testcompany@example.com')
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.get().user.email, 'testcompany@example.com')

class InvitationTests(APITestCase):
    def setUp(self):
        self.company_user = User.objects.create_user(email='company@example.com', password='companypassword', is_company=True)
        if not Company.objects.filter(user=self.company_user).exists():
            self.company = Company.objects.create(user=self.company_user, companyName='Test Company')
        else:
            self.company = Company.objects.get(user=self.company_user)
        self.client.login(email='company@example.com', password='companypassword')

    def test_create_invitation(self):
        url = reverse('invitation-list')
        data = {
            'email': 'invitee@example.com',
            'company': self.company.id
        }
        self.client.force_authenticate(user=self.company_user)
        response = self.client.post(url, data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print("Response Data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invitation.objects.count(), 1)
        self.assertEqual(Invitation.objects.get().email, 'invitee@example.com')

    def test_accept_invitation(self):
        invitation = Invitation.objects.create(email='invitee@example.com', company=self.company, invited_by=self.company_user, token=uuid.uuid4())
        url = reverse('invitation-accept', args=[str(invitation.token)])
        self.client.force_authenticate(user=self.company_user)
        response = self.client.post(url, {}, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print("Response Data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Invitation.objects.get(id=invitation.id).is_accepted)
        self.assertEqual(User.objects.count(), 2)
        self.assertTrue(User.objects.get(email='invitee@example.com').is_active)
        self.assertEqual(CompanyMember.objects.count(), 1)
        self.assertEqual(CompanyMember.objects.get().user.email, 'invitee@example.com')

if __name__ == "__main__":
    import unittest
    unittest.main()