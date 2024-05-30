from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Role, UserRole, Permission, RolePermission

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Additional info', {'fields': ('keywords', 'procurement_categories')}),
    )

admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Role)
admin.site.register(RolePermission)
admin.site.register(Permission)
admin.site.register(UserRole)