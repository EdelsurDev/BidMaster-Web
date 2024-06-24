from functools import wraps
from django.http import HttpResponseForbidden
from usuarios.models import Permission
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser

def permission_required(permission_codename):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You do not have permission to access this page.")
            
            user_permissions = Permission.objects.filter(
                rolepermission__role__userrole__user=request.user,
                codename=permission_codename
            ).exists()
            
            if not user_permissions:
                return HttpResponseForbidden("You do not have permission to access this page.")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def firebase_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return JsonResponse({'error': 'Authentication required'}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
