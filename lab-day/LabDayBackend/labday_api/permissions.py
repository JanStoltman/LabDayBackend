from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return IsAdmin.has_permission(request, view)


class IsAdmin(BaseException):
    def has_permission(self, request, view):
        return request.user.is_staff
