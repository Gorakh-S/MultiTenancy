from django.contrib import admin
from .models import Tenant, Organization, Department, Customer

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('tenant_id', 'domain', 'is_active', 'created_at', 'updated_at')
    search_fields = ('tenant_id', 'domain')
    list_filter = ('is_active', 'created_at')
    ordering = ('-created_at',)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'tenant', 'created_at', 'updated_at')
    search_fields = ('name', 'tenant__domain')
    list_filter = ('tenant',)
    ordering = ('-created_at',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'created_at', 'updated_at')
    search_fields = ('name', 'organization__name')
    list_filter = ('organization',)
    ordering = ('-created_at',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'department', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'department__name')
    list_filter = ('department',)
    ordering = ('-created_at',)
