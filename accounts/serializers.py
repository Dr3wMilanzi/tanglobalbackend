from rest_framework import serializers
from .models import CompanyContactDetails, CustomUser, Invitation, PaymentPlan
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer

class PaymentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPlan
        fields = '__all__'

class CompanyContactDetailsSerializer(serializers.ModelSerializer):
    is_profile_complete = serializers.SerializerMethodField()
    plan_details = PaymentPlanSerializer(source='plan', read_only=True)

    class Meta:
        model = CompanyContactDetails
        fields = '__all__'
        read_only_fields = ['user']

    def get_is_profile_complete(self, obj):
        # Assuming you have a method `is_profile_complete` in the model
        return obj.is_profile_complete()

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = '__all__'

class UserSerializer(BaseUserSerializer):
    company_details = CompanyContactDetailsSerializer(source='company', read_only=True)
    plan_details = PaymentPlanSerializer(source='plan', read_only=True)
    invitations = InvitationSerializer(source='invitations_sent', many=True, read_only=True)

    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = BaseUserSerializer.Meta.fields + (
            'full_name', 'phone_number', 'address', 'profile_picture', 'is_individual', 
            'is_company', 'company', 'company_details', 'plan', 'plan_details', 
            'plan_paid', 'plan_expiry_date', 'invitations'
        )

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = CustomUser
        fields = BaseUserCreateSerializer.Meta.fields + (
            'full_name', 'phone_number', 'address', 'profile_picture', 
            'is_individual', 'is_company', 'company'
        )