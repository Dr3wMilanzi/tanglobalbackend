from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Company

class CompanyInline(admin.StackedInline):  # or admin.TabularInline
    model = Company
    can_delete = False
    verbose_name_plural = 'Company Contact Details'

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'full_name', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active', 
            'is_staff', 
            'is_superuser',
            'groups', 
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password')
            }
        ),
    )
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

    list_display = ('email', 'full_name', 'is_staff', 'is_superuser', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('email', 'full_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    inlines = [CompanyInline]

# Register CustomUser model with the UserAdmin
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Company)
