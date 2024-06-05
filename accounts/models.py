from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django_resized import ResizedImageField

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

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,blank=False,null=False)
    full_name = models.CharField(max_length=180,blank=True,null=True)
    is_individual = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # is_active_membership = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class CompanyContactDetails(models.Model):
    COMPANY_TYPES = (
        ('Fleet Company', 'Fleet Company'),
        ('Cargo Company', 'Cargo Company'),
    )
     
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPES,default="Fleet Company")
    companyName = models.CharField(max_length=100)
    comapnyTelephone = models.CharField(max_length=100)
    comapnyEmail = models.EmailField(max_length=100)
    comapnyWebsite = models.URLField(max_length=100)
    companyAddress = models.TextField()
    tin = models.CharField(max_length=100, blank=True, null=True)
    vat = models.CharField(max_length=100, blank=True, null=True)
    companyreg = models.CharField(max_length=100, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    company = ResizedImageField(size=[300, 300], upload_to='comapny/logo',quality=75,force_format='PNG',blank=True, null=True)

    def __str__(self):
        return self.companyName
    
    def isProfileComplete(self):
        # Check if any required fields are None or empty
        if (
            not self.company_type and
            not self.companyName and
            not self.comapnyTelephone and
            not self.comapnyEmail and
            not self.comapnyWebsite and
            not self.companyAddress and 
            not self.tin and
            not self.vat and
            not self.company
        ):
            return False

        return True
    

@receiver(post_save, sender=CustomUser)
def create_company_details(sender, instance, created, **kwargs):
    if created and instance.is_company:
        CompanyContactDetails.objects.create(user=instance, companyName="Update Your Company Name")



class Membership(models.Model):
    MEMBERSHIP_TYPES = (
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_TYPES)
    expiration_date = models.DateField()
    is_active = models.BooleanField(default=True)  # Default membership status is active
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_active(self):
        return self.expiration_date >= timezone.now().date()
    
    def is_expired(self):
        return self.expiration_date < timezone.now().date()

@receiver(post_save, sender=Membership)
def update_user_membership_status(sender, instance, created, **kwargs):
    """
    Automatically update the user's status based on their membership status.
    """
    if instance.is_active and instance.is_expired():
        # If membership is active but expired, set user status to inactive
        instance.user.is_active = False
        instance.user.save()
    elif not instance.is_active and not instance.is_expired():
        # If membership is inactive but not expired, set user status to active
        instance.user.is_active = True
        instance.user.save()