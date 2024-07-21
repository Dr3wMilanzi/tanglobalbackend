from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserOnboardingViewSet, CompanyViewSet, CompanyMemberViewSet, InvitationViewSet, PaymentPlanViewSet

router = DefaultRouter()
router.register(r'onboarding', UserOnboardingViewSet, basename='onboarding')
router.register(r'', CompanyViewSet)
router.register(r'company-members', CompanyMemberViewSet)
router.register(r'invitations', InvitationViewSet)
router.register(r'payment-plans', PaymentPlanViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('invitations/<uuid:pk>/accept/', InvitationViewSet.as_view({'post': 'accept_invitation'}), name='invitation-accept'),
]