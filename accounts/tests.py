from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import CustomUser, CompanyContactDetails, Invitation, PaymentPlan, CompanyMembership
from .serializers import UserCreateSerializer
from django.utils.crypto import get_random_string

class UserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='test@example.com', password='password', is_company=True)
        self.client.force_authenticate(user=self.user)

    def test_list_users(self):
        response = self.client.get(reverse('customuser-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activate_user(self):
        response = self.client.post(reverse('customuser-activate', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_deactivate_user(self):
        response = self.client.post(reverse('customuser-deactivate', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

class CompanyContactDetailsTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='company@example.com', password='password', is_company=True)
        self.company = CompanyContactDetails.objects.create(
            user=self.user,
            company_type='Fleet Company',
            companyName='Test Company',
            companyTelephone='123456789',
            companyEmail='info@testcompany.com',
            companyWebsite='http://testcompany.com',
            companyAddress='Test Address'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_company_details(self):
        response = self.client.get(reverse('companycontactdetails-detail', kwargs={'pk': self.company.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['companyName'], 'Test Company')

class InvitationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='company@example.com', password='password', is_company=True)
        self.company = CompanyContactDetails.objects.create(
            user=self.user,
            company_type='Fleet Company',
            companyName='Test Company',
            companyTelephone='123456789',
            companyEmail='info@testcompany.com',
            companyWebsite='http://testcompany.com',
            companyAddress='Test Address'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_invitation(self):
        data = {
            'email': 'invitee@example.com',
            'company': self.company.pk
        }
        response = self.client.post(reverse('invitation-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Invitation.objects.filter(email='invitee@example.com').exists())

    def test_accept_invitation(self):
        invitation = Invitation.objects.create(
            email='invitee@example.com',
            company=self.company,
            invited_by=self.user,
            token=get_random_string(50)
        )
        data = {'token': invitation.token}
        response = self.client.post(reverse('invitation-accept-invitation', kwargs={'token': invitation.token}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        invitation.refresh_from_db()
        self.assertTrue(invitation.is_accepted)
        self.assertTrue(CustomUser.objects.filter(email='invitee@example.com').exists())
        self.assertTrue(CompanyMembership.objects.filter(user__email='invitee@example.com', company=self.company).exists())

class PaymentPlanTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='admin@example.com', password='password', is_staff=True)
        self.client.force_authenticate(user=self.user)

    def test_list_payment_plans(self):
        response = self.client.get(reverse('paymentplan-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_payment_plan(self):
        plan = PaymentPlan.objects.create(
            name='Standard Plan',
            plan_type='individual',
            price=99.99,
            duration_days=30
        )
        response = self.client.get(reverse('paymentplan-detail', kwargs={'pk': plan.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Standard Plan')

class UserOnboardingTests(APITestCase):
    def test_user_onboarding(self):
        data = {
            "email": "newuser@example.com",
            "password": "password",
            "full_name": "New User",
            "company_name": "New User's Company"
        }
        response = self.client.post(reverse('onboarding-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email='newuser@example.com').exists())
        self.assertTrue(CompanyContactDetails.objects.filter(companyName="New User's Company").exists())