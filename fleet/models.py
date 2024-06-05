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
    
        
class Vehicle(models.Model):
    company = models.ForeignKey(CompanyContactDetails,on_delete=models.SET_NULL,blank=True, null=True)
    capacity = models.DecimalField(max_digits=10,decimal_places=2) #in tones
    platenumber = models.CharField(max_length=100) #in tones
    isInsuared = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.vehicle_type} ({self.capacity})"

class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='images', on_delete=models.CASCADE)
    image = ResizedImageField(size=[500, 300], upload_to='vehicles/images',quality=75,force_format='PNG')
    
    def __str__(self):
        pass
        # return f"Image for {self.vehicle}"