from django.db import models
from django.utils.text import slugify
from django_resized import ResizedImageField
from accounts.models import CompanyContactDetails


class VehicleType(models.Model):
    name = models.CharField(max_length=180)
    slug = models.SlugField(blank=False, null=True, unique=True, editable=False)

    def save(self, *args, **kwargs):
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
    
class VehicleImage(models.Model):
    image = ResizedImageField(size=[500, 300], upload_to='vehicles/images',quality=75,force_format='PNG')
    
    def __str__(self):
        return f"Image for {self.vehicle.vehicle_type}"
        

class Vehicle(models.Model):
    vehicleTypes = models.ManyToManyField(VehicleType, related_name='vehicles')
    company = models.ForeignKey(CompanyContactDetails,on_delete=models.SET_NULL,blank=True, null=True)
    capacity = models.DecimalField(max_digits=10,decimal_places=2) #in tones
    platenumber = models.CharField(max_length=100) #in tones
    isInsuared = models.BooleanField(default=True)
    images = models.ForeignKey(VehicleImage, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.vehicle_type} ({self.capacity})"

