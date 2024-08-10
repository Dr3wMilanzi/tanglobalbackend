from rest_framework import viewsets, status
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser,IsAuthenticatedOrReadOnly
from .permissions import IsCompany
from rest_framework.decorators import action
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser, Company, CompanyMember, Invitation, PaymentPlan
from .serializers import UserSerializer, CustomUserCreateSerializer, CompanySerializer, CompanyMemberSerializer, InvitationSerializer, PaymentPlanSerializer
import logging

logger = logging.getLogger(__name__)

class UserOnboardingViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = CustomUserCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        logger.info(f"New user created with email {user.email}.")
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser, IsCompany], url_path='approve')
    def approve_user(self, request, pk=None):
        try:
            user = self.get_object()
            user.is_active = True
            user.save()
            logger.info(f"User {user.email} has been approved.")
            return Response({"detail": "User has been approved."}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error approving user: {str(e)}")
            return Response({"detail": "An error occurred while approving the user."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser, IsCompany], url_path='disapprove')
    def disapprove_user(self, request, pk=None):
        try:
            user = self.get_object()
            user.is_active = False
            user.save()
            logger.info(f"User {user.email} has been disapproved.")
            return Response({"detail": "User has been disapproved."}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error disapproving user: {str(e)}")
            return Response({"detail": "An error occurred while disapproving the user."}, status=status.HTTP_400_BAD_REQUEST)

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CompanyMemberViewSet(viewsets.ModelViewSet):
    queryset = CompanyMember.objects.all()
    serializer_class = CompanyMemberSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invitation = serializer.save(invited_by=request.user)
        self.send_invitation_email(invitation)
        logger.info(f"Invitation sent to {invitation.email} by {request.user.email}.")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def send_invitation_email(self, invitation):
        subject = "You're invited to join our platform"
        message = f"Please accept the invitation by clicking the following link: {settings.FRONTEND_URL}/accept-invitation/{invitation.token}/"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [invitation.email])

    @action(detail=False, methods=['post'], url_path='accept/(?P<token>[0-9a-f-]+)')
    def accept_invitation(self, request, token=None):
        try:
            invitation = Invitation.objects.get(token=token)
            if invitation.is_accepted:
                return Response({"detail": "Invitation already accepted."}, status=status.HTTP_400_BAD_REQUEST)
            user = CustomUser.objects.create(email=invitation.email, is_active=True)
            CompanyMember.objects.create(user=user, company=invitation.company)
            invitation.is_accepted = True
            invitation.save()
            logger.info(f"Invitation accepted by {invitation.email}.")
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        except Invitation.DoesNotExist:
            logger.error(f"Invitation with token {token} does not exist.")
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error accepting invitation: {str(e)}")
            return Response({"detail": "An error occurred while accepting the invitation."}, status=status.HTTP_400_BAD_REQUEST)
        
        

class PaymentPlanViewSet(viewsets.ModelViewSet):
    queryset = PaymentPlan.objects.all()
    serializer_class = PaymentPlanSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    
class Homepage(TemplateView):
    template_name = "index.html" 