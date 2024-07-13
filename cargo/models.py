from django.db import models
from django.utils.text import slugify
from django_resized import ResizedImageField
import uuid

class CargoType(models.Model):
    name = models.CharField(max_length=180)
    slug = models.SlugField(unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Cargo(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, blank=True,editable=False)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    cargo_type = models.ForeignKey(CargoType, related_name='cargos', on_delete=models.CASCADE)
    
    WEIGHT_UNIT_CHOICES = [
        ('kg', 'Kilograms'),
        ('ltr', 'Liters'),
    ]
    weight_unit = models.CharField(max_length=3, choices=WEIGHT_UNIT_CHOICES, default='kg')
    length = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    cargo = models.CharField(max_length=255)
    fragile = models.BooleanField(default=False)
    temperature_sensitive = models.BooleanField(default=False)
    special_handling_instructions = models.TextField(blank=True, null=True)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    receiver_name = models.CharField(max_length=255)
    receiver_contact = models.CharField(max_length=255)
    sender_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('delayed', 'Delayed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.origin}-{self.destination}-{self.cargo}-{str(uuid.uuid4())[:8]}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cargo} - {self.weight}{self.weight_unit}"

class CargoDocument(models.Model):
    cargo = models.ForeignKey(Cargo, related_name='cargo_documents', on_delete=models.CASCADE)
    file = models.FileField(upload_to='cargo/documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.cargo.cargo} ({self.uploaded_at})"

class CargoImage(models.Model):
    cargo = models.ForeignKey(Cargo, related_name='images', on_delete=models.CASCADE)
    image = ResizedImageField(size=[500, 300], upload_to='cargo/images', quality=75, force_format='PNG')
    
    def __str__(self):
        return f"Image for {self.cargo.cargo} ({self.image})"
    
class CargoTracking(models.Model):
    cargo = models.ForeignKey(Cargo, related_name='tracking_info', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=Cargo.STATUS_CHOICES)
    location = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cargo.cargo} - {self.status} at {self.location}"