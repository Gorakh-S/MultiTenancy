from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from core.models import Tenant

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Skip tenant check for specific paths
        skip_paths = [
            '/api/token-auth/',
            '/api/token/',
            '/api/token/refresh/',
            '/admin/',
            '/api/tenants/',
        ]
        if any(request.path.startswith(path) for path in skip_paths):
            return

        # Get tenant domain from headers
        domain = request.headers.get("X-Tenant-Domain")
        if not domain:
            return JsonResponse({"error": "Missing X-Tenant-Domain header"}, status=400)

        try:
            tenant = Tenant.objects.get(domain=domain, is_active=True)
            request.tenant = tenant
        except Tenant.DoesNotExist:
            return JsonResponse({"error": "Invalid tenant domain"}, status=400)
