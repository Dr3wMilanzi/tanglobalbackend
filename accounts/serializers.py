from djoser.serializers import UserSerializer
from rest_framework import serializers
from .models import CompanyContactDetails, Membership,CustomUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class CompanyContactDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyContactDetails
        fields = '__all__'

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'

class CustomUserSerializer(UserSerializer):
    company_details = CompanyContactDetailsSerializer(source='companycontactdetails', read_only=True)
    memberships = MembershipSerializer(source='membership', read_only=True)

    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ('id','full_name','email','is_superuser','is_staff','is_individual','is_cargo_owner','is_fleet_owner','is_company','memberships','company_details',)

class CustomUserCreateSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ('full_name','email','is_individual','is_cargo_owner','is_fleet_owner','is_company')

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(write_only=True, validators=[validate_password],style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('full_name','email','password','is_individual','is_cargo_owner','is_fleet_owner','is_company')
        
        

    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['email'], 
        validated_data['password']
        )
        user.full_name = validated_data['full_name']
        user.is_individual = validated_data['is_individual']
        user.typeofmember = validated_data['typeofmember']
        user.is_cargo_owner = validated_data['is_cargo_owner']
        user.is_fleet_owner = validated_data['is_fleet_owner']
        user.is_company = validated_data['is_company']
        user.save()
        return user