from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """ Разрешение, разрешающее редактировать только себя. """

    def has_object_permission(self, request, view, obj):
        return obj.email == request.user.email
