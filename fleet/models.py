from django.db import models
from django.utils.text import slugify
from django_resized import ResizedImageField
from accounts.models import Company,CompanyMember
from django.conf import settings
from cargo.models import Cargo
import uuid
from django.utils import timezone


class VehicleType(models.Model):
    name = models.CharField(max_length=180)
    slug = models.SlugField(blank=False, null=True, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            count = 1
            slug = self.slug
            while VehicleType.objects.filter(slug=slug).exists():
                slug = f"{self.slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Driver(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100)
    license_expiry_date = models.DateField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.get_full_name()
    
class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='created_vehicles', blank=True, null=True)
    CARGO_OWNER_TYPE = [
        ('Personal', 'Personal'),
        ('Company', 'Company'),
    ]
    owner_type = models.CharField(max_length=10, choices=CARGO_OWNER_TYPE, default='Personal')
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, related_name="vehicle_type")
    capacity = models.DecimalField(max_digits=10, decimal_places=2)  # in tons
    plate_number = models.CharField(max_length=100, unique=True, blank=False, null=False)
    is_insured = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='approved_vehicles', blank=True, null=True)
    manufacture_year = models.IntegerField(blank=True, null=True)
    registration_date = models.DateField(blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    make = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Add default value here
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.make}-{self.model}-{self.plate_number}")
            count = 1
            slug = self.slug
            while Vehicle.objects.filter(slug=slug).exists():
                slug = f"{self.slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.vehicle_type} ({self.capacity} tons) - {self.plate_number}"

    def approve(self, user):
        self.is_approved = True
        self.approved_by = user
        self.save()

class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='images', on_delete=models.CASCADE)
    image = ResizedImageField(size=[500, 300], upload_to='vehicles/images', quality=75, force_format='PNG')
    
    def __str__(self):
        return f"Image for {self.vehicle}"

class Trip(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    start_km = models.DecimalField(max_digits=10, decimal_places=2)  # Odometer reading at the start of the trip
    finish_km = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Odometer reading at the end of the trip
    fuel_consumption = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Fuel consumed during the trip
    cargo_description = models.TextField()
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField(blank=True, null=True)
    service_interval_km = models.DecimalField(max_digits=10, decimal_places=2, default=10000)  # Interval in kilometers for the next recommended service

    def __str__(self):
        return f"Trip from {self.origin} to {self.destination} by {self.vehicle.plate_number}"

    @property
    def distance_covered(self):
        if self.finish_km and self.start_km:
            return self.finish_km - self.start_km
        return None

    @property
    def next_service_due(self):
        if self.finish_km:
            next_service_km = (self.finish_km // self.service_interval_km + 1) * self.service_interval_km
            return next_service_km
        return None