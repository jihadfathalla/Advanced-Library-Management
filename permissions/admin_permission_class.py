from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            if "Admin" in request.user.groups.all().values_list("name", flat=True):
                return True
        except Exception:
            pass
