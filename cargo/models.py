from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
import uuid

class CargoDocument(models.Model):
    documentName = models.CharField(max_length=180)
    documentFile = models.FileField(upload_to='cargo/file/')

class CargoType(models.Model):
    name = models.CharField(max_length=180)
    slug = models.SlugField(blank=False, null=True, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Cargo(models.Model):
    cargo_type = models.ForeignKey(CargoType, on_delete=models.SET_NULL, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(blank=False, null=True, unique=True, editable=False)
    weight = models.DecimalField(max_digits=10, decimal_places=2)  # in kilograms
    dimensions = models.CharField(max_length=50)  # e.g., "10x5x3 meters"
    cargo = models.CharField(max_length=50,default="Laguage name",blank=False,null=False)  # e.g., "10x5x3 meters"
    fragile = models.BooleanField(default=False)
    temperature_sensitive = models.BooleanField(default=False)
    special_handling_instructions = models.TextField(blank=True)
    origin = models.CharField(max_length=100)  # Origin location
    destination = models.CharField(max_length=100)  # Destination location
    sender_name = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    receiver_name = models.CharField(max_length=100)  # Name of the receiver
    receiver_contact = models.CharField(max_length=20)  # Contact information of the receiver
    added_at = models.DateTimeField(default=timezone.now)  # Contact information of the receiver
    pickupdate = models.DateField(default=timezone.now)  # Contact information of the receiver
    delivery_date = models.DateField(null=True, blank=True)  # Expected delivery date
    actual_delivery_date = models.DateField(null=True, blank=True)  # Actual delivery date
    status_choices = [
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('delayed', 'Delayed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=50, choices=status_choices, default='pending')
    cargo_document = models.ForeignKey(CargoDocument, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(self.uuid)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cargo_type.name} - {self.weight}kg"
