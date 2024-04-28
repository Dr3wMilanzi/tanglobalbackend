from django.contrib import admin
from .models import CustomUser, CompanyContactDetails

admin.site.register(CustomUser)
admin.site.register(CompanyContactDetails)
