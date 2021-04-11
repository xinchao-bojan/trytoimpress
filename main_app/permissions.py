from rest_framework.permissions import BasePermission, IsAuthenticated


class IsAdmin(BasePermission):
    message = 'It is wrong neighborhood for u (admin)'

    def has_permission(self, request, view):
        return IsAuthenticated and request.user.is_admin


class IsOwner(BasePermission):
    message = 'It is wrong neighborhood for u (owner)'

    def has_object_permission(self, request, view, obj):
        return IsAuthenticated and obj.user == request.user
