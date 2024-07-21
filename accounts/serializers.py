from rest_framework import serializers
from .models import CustomUser, Company, CompanyMember, Invitation, PaymentPlan

class PaymentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPlan
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class CompanyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyMember
        fields = '__all__'

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    company_details = CompanySerializer(source='company', read_only=True)
    invitations = InvitationSerializer(source='invitations_sent', many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'full_name', 'phone_number', 'address', 'profile_picture', 'is_individual',
            'is_company','is_superuser', 'is_staff', 'is_active', 'company_details', 'invitations'
        ]

class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'email', 'password', 'full_name', 'phone_number', 'address', 'profile_picture', 
            'is_individual', 'is_company'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user