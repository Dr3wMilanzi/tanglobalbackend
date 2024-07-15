from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django_resized import ResizedImageField
import uuid
import logging

logger = logging.getLogger(__name__)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class PaymentPlan(models.Model):
    PLAN_CHOICES = (
        ('individual', 'Individual'),
        ('company', 'Company'),
    )
    name = models.CharField(max_length=255)
    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()  # Duration of the plan in days

    def __str__(self):
        return f"{self.name} ({self.plan_type})"

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    full_name = models.CharField(max_length=180, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_individual = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def approve(self):
        self.is_approved = not self.is_approved
        self.save()
    
    def disapprove(self):
        self.is_approved = not self.is_approved
        self.save()

class Company(models.Model):
    COMPANY_TYPES = (
        ('Fleet Company', 'Fleet Company'),
        ('Cargo Company', 'Cargo Company'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPES, default="Fleet Company")
    companyName = models.CharField(max_length=100)
    companyTelephone = models.CharField(max_length=100)
    companyEmail = models.EmailField(max_length=100)
    companyWebsite = models.URLField(max_length=100)
    companyAddress = models.TextField()
    tin = models.CharField(max_length=100, blank=True, null=True)
    vat = models.CharField(max_length=100, blank=True, null=True)
    companyreg = models.CharField(max_length=100, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    company = ResizedImageField(size=[300, 300], upload_to='company/logo', quality=75, force_format='PNG', blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)
    operating_hours = models.CharField(max_length=100, blank=True, null=True)
    social_media_links = models.JSONField(blank=True, null=True)
    

    def __str__(self):
        return self.companyName

class CompanyMember(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.company.companyName}"

class Invitation(models.Model):
    email = models.EmailField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invitations_sent')
    date_invited = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Invitation to {self.email} for {self.company.companyName}"

    def accept(self, user):
        if not self.is_accepted:
            self.is_accepted = True
            self.save()
            Company.objects.create(user=user, company=self.company)

@receiver(post_save, sender=CustomUser)
def create_company_details(sender, instance, created, **kwargs):
    if created and instance.is_company:
        Company.objects.create(user=instance, companyName="Update Your Company Name")

@receiver(post_save, sender=Invitation)
def send_invitation_email(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Sending invitation email to {instance.email} for company {instance.company.companyName}")
        # Logic to send email invitation with the token
        pass  # Implement the email sending logic here
    
# class CompanyMembership(models.Model):
#     MEMBERSHIP_TYPES = (
#         ('basic', 'Basic'),
#         ('premium', 'Premium'),
#     )

#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_TYPES)
#     expiration_date = models.DateField()
#     is_active = models.BooleanField(default=True)  # Default membership status is active
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def is_active(self):
#         return self.expiration_date >= timezone.now().date()
    
#     def is_expired(self):
#         return self.expiration_date < timezone.now().date()