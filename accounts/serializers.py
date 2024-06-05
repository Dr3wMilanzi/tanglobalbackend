from rest_framework import serializers
from .models import CompanyContactDetails, Membership, CustomUser

class CompanyContactDetailsSerializer(serializers.ModelSerializer):
    is_profile_complete = serializers.SerializerMethodField()
    class Meta:
        model = CompanyContactDetails
        fields = '__all__'
        read_only_fields = ['user']

    def get_is_profile_complete(self, obj):
        return obj.isProfileComplete()

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    company_details = CompanyContactDetailsSerializer(source='companycontactdetails', read_only=True)
    memberships = MembershipSerializer(source='membership', read_only=True)
    is_active_membership = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'full_name', 'email', 'is_superuser', 'is_staff', 'is_individual','is_company', 'is_active_membership', 'memberships', 'company_details')

    def get_is_active_membership(self, obj):
        # Check if the user has a related Membership instance
        if hasattr(obj, 'membership'):
            # Get the related Membership instance for the user
            membership_instance = obj.membership
            # Check if the membership is active
            return membership_instance.is_active()
        else:
            # If no related Membership instance exists, return False
            return False
    

class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('full_name', 'email', 'is_individual','is_company')

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('full_name', 'email', 'password', 'is_individual','is_company')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', ''),
            is_individual=validated_data.get('is_individual', False),
            is_company=validated_data.get('is_company', False)
        )
        return user
