from django.contrib import admin
from .models import Vehicle,VehicleType,VehicleImage
# Register your models here.
admin.site.register(Vehicle)
admin.site.register(VehicleType)
admin.site.register(VehicleImage)