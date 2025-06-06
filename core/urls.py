from rest_framework.routers import DefaultRouter
from django.urls import path, include
from core.api import TenantViewSet, OrganizationViewSet, DepartmentViewSet, CustomerViewSet

router = DefaultRouter()
router.register(r'tenants', TenantViewSet, basename='tenant')
router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'customers', CustomerViewSet, basename='customer')
urlpatterns = [
    path('api/', include(router.urls)),
]