from rest_framework.permissions import BasePermission


class IsBoxOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user == request.user.box.owner) or bool(
            request.user and request.user.is_staff
        )

    def has_object_permission(self, request, view, alert):
        return bool(request.user == request.user.box.owner) or bool(
            request.user and request.user.is_staff
        )
