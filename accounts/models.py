from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    email = models.EmailField(unique=True)
    is_individual = models.BooleanField(default=False)
    is_cargo_owner = models.BooleanField(default=False)
    is_fleet_owner = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class CompanyContactDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    companyName = models.CharField(max_length=100)
    comapnyTelephone = models.CharField(max_length=100)
    comapnyEmail = models.CharField(max_length=100)
    comapnyWebsite = models.CharField(max_length=100)
    companyAddress = models.TextField()
    tin = models.CharField(max_length=100, blank=True, null=True)
    vat = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.companyName
    

@receiver(post_save, sender=CustomUser)
def create_company_details(sender, instance, created, **kwargs):
    if created and instance.is_cargo_owner or instance.is_fleet_owner:
        CompanyContactDetails.objects.create(user=instance, company_name="Update Your Company Name")