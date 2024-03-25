from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """ Разрешение, разрешающее редактировать только владельцам объекта. """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
