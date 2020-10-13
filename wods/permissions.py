from rest_framework.permissions import BasePermission


class IsBoxOwner(BasePermission):

    """ Wod에 연결된 box의 owner와 수정하려는 user가 동일한지 """

    # List, Retrieve - AllowAny

    # Destry, Update, Partial update
    def has_object_permission(self, request, view, wod):
        return bool(request.user == request.user.box.owner)

    # Create
    def has_permission(self, request, view):
        return bool(request.user == request.user.box.owner)