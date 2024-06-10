from django.contrib import admin
from .models import Update,UpdateType,SelectedUpdatesByUser
# Register your models here.

admin.site.register(Update)
admin.site.register(UpdateType)
admin.site.register(SelectedUpdatesByUser)