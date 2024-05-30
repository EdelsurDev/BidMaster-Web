from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from usuarios.models import Permission, RolePermission

class PermissionRequiredMixin:
    required_permission = None

    def has_permission(self, user):
        if self.required_permission is None:
            return True
        return RolePermission.objects.filter(
            role__userrole__user=user,
            permission__codename=self.required_permission
        ).exists()

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission(request.user):
            return HttpResponseForbidden("You do not have permission to view this content.")
        return super().dispatch(request, *args, **kwargs)