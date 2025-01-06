from rest_framework.permissions import BasePermission


class IsAdminOrLibrarian(BasePermission):
    def has_permission(self, request, view):
        try:
            if "Admin" or "Librarian" in request.user.groups.all().values_list(
                "name", flat=True
            ):
                return True
        except Exception:
            pass
