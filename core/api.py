from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Tenant, Organization, Department, Customer
from core.serializers import TenantSerializer, OrganizationSerializer, DepartmentSerializer, CustomerSerializer
from rest_framework.exceptions import PermissionDenied


class TenantViewSet(viewsets.ModelViewSet):
    
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]


class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        tenant_id = self.request.tenant.tenant_id
        return Organization.objects.filter(tenant__tenant_id=tenant_id)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant)


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Department.objects.filter(organization__tenant=self.request.tenant)

    def perform_create(self, serializer):
        org = serializer.validated_data['organization']
        if org.tenant != self.request.tenant:
            raise PermissionDenied("You are not allowed to create departments in this organization.")
        serializer.save()

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Customer.objects.filter(department__organization__tenant=self.request.tenant)

    def perform_create(self, serializer):
        dept = serializer.validated_data['department']
        if dept.organization.tenant != self.request.tenant:
            raise PermissionDenied("You are not allowed to create customers in this department.")
        serializer.save()