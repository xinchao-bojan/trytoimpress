from rest_framework.permissions import BasePermission, IsAuthenticated


class IsAdmin(BasePermission):
    message = 'It is wrong neighborhood for u (is_staff)'

    def has_permission(self, request, view):
        return request.user.is_staff


class IsOwner(BasePermission):
    message = 'It is wrong neighborhood for u (owner)'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
