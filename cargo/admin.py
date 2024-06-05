from django.contrib import admin
from .models import Cargo,CargoDocument,CargoType
# Register your models here.
admin.site.register(Cargo)
admin.site.register(CargoType)
admin.site.register(CargoDocument)
