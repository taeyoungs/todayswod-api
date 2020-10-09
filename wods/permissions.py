from rest_framework.permissions import BasePermission


class IsBoxOwner(BasePermission):

    """ Wod에 연결된 box의 owner와 수정하려는 user가 동일한지 """

    def has_object_permission(self, request, view, wod):
        print(request.user.box.owner)
        return request.user == request.user.box.owner