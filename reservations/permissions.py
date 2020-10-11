from rest_framework.permissions import BasePermission


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, reservation):
        return request.user == reservation.user


class IsSelfOrBoxOwnerOrAdminUser(BasePermission):
    """ IsSelf, IsBoxOwner, IsAdminUser """

    def has_object_permission(self, request, view, reservation):
        return bool(request.user and request.user.is_staff) or bool(request.user == reservation.user) or bool(request.user == request.user.box.owner)