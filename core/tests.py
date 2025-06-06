from django.test import TestCase
# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from core.models import Tenant, Organization, Department, Customer

class MultiTenantTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        # Create tenants
        self.tenant1 = Tenant.objects.create(tenant_id='tenant1', domain='tenant1.com')
        self.tenant2 = Tenant.objects.create(tenant_id='tenant2', domain='tenant2.com')

        # Create users
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')

        # Generate JWT token
        from rest_framework_simplejwt.tokens import RefreshToken
        token = RefreshToken.for_user(self.user1)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token.access_token}',
            HTTP_X_TENANT_DOMAIN='tenant1.com'
        )

        # Create organization and related data
        self.org1 = Organization.objects.create(tenant=self.tenant1, name='Org1')
        self.dept1 = Department.objects.create(organization=self.org1, name='Dept1')
        self.cust1 = Customer.objects.create(department=self.dept1, name='Gorakh', email='gorakh1@gmail.com')
