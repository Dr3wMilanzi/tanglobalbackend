from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .models import PaymentPlan, CustomUser, CompanyContactDetails, CompanyMembership, Invitation
from .serializers import PaymentPlanSerializer, CustomUserSerializer, CompanyContactDetailsSerializer, CompanyMembershipSerializer, InvitationSerializer, UserCreateSerializer
from .permissions import IsCompany

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CompanyContactDetailsViewSet(viewsets.ModelViewSet):
    queryset = CompanyContactDetails.objects.all()
    serializer_class = CompanyContactDetailsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = [IsCompany]

    def accept_invitation(self, request, token):
        try:
            invitation = Invitation.objects.get(token=token)
            if invitation.is_accepted:
                return Response({"detail": "Invitation already accepted."}, status=status.HTTP_400_BAD_REQUEST)

            user = CustomUser.objects.get(email=invitation.email)
            invitation.is_accepted = True
            invitation.save()

            # Add the user to the company's membership
            CompanyMembership.objects.create(user=user, company=invitation.company)

            return Response({"detail": "Invitation accepted."}, status=status.HTTP_200_OK)
        except Invitation.DoesNotExist:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        if not request.user.is_company:
            return Response({"detail": "Only company owners can invite users."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data['invited_by'] = request.user.id
        data['token'] = get_random_string(50)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(

raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Add logic to send email invitation with the token here
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PaymentPlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentPlan.objects.all()
    serializer_class = PaymentPlanSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class UserOnboardingViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)