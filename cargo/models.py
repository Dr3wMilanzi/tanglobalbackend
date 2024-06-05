from django.db import models
from django.conf import settings
from django.utils.text import slugify
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
    cargo_type = models.ManyToManyField(CargoType, related_name="cargos")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, editable=False)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    dimensions = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50, default="Luggage name")
    fragile = models.BooleanField(default=False)
    temperature_sensitive = models.BooleanField(default=False)
    special_handling_instructions = models.TextField(blank=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    sender_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    receiver_name = models.CharField(max_length=100)
    receiver_contact = models.CharField(max_length=20)
    status_choices = [
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('delayed', 'Delayed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=50, choices=status_choices, default='pending')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(self.uuid)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cargo} - {self.weight}kg"

class CargoDocument(models.Model):
    documentName = models.CharField(max_length=180)
    cargo = models.ForeignKey(Cargo, related_name='cargo_documents', on_delete=models.CASCADE)
    documentFile = models.FileField(upload_to='cargo/file/')

    def __str__(self):
        return self.name