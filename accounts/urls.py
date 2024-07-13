from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentPlanViewSet, CustomUserViewSet, CompanyContactDetailsViewSet, InvitationViewSet, CompanyMembershipViewSet, UserOnboardingViewSet

router = DefaultRouter()
router.register(r'payment-plans', PaymentPlanViewSet)
router.register(r'users', CustomUserViewSet)
router.register(r'company-contacts', CompanyContactDetailsViewSet)
router.register(r'company-memberships', CompanyMembershipViewSet)
router.register(r'invitations', InvitationViewSet)
router.register(r'onboarding', UserOnboardingViewSet, basename='onboarding')

urlpatterns = [
    path('', include(router.urls)),
]