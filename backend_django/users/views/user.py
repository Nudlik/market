from djoser import views
from rest_framework.permissions import AllowAny, IsAdminUser

from users.pagination import UserPagination
from users.permissions import IsOwner
from users.serializers import UserSerializer, UserRegistrationSerializer


class OverrideMethodsMeta(type):
    set_none = {
        'activation',
        'resend_activation',
        'set_username',
        'reset_username',
        'reset_username_confirm',
    }

    def __new__(mcs, name, bases, dct):
        for base in bases:
            for attr_name in dir(base):
                attr = getattr(base, attr_name)
                if callable(attr) and not attr_name.startswith("__") and attr_name in mcs.set_none:
                    dct[attr_name] = lambda self, *args, **kwargs: None
        return super().__new__(mcs, name, bases, dct)


class UserViewSet(views.UserViewSet, metaclass=OverrideMethodsMeta):
    pagination_class = UserPagination
    perms_methods = {
        'create': [AllowAny],
        'update': [IsOwner | IsAdminUser],
        'partial_update': [IsOwner | IsAdminUser],
        'destroy': [IsOwner | IsAdminUser],
    }
    choice_serializer = {
        'create': UserRegistrationSerializer,
        'list': UserSerializer,
        'me': UserSerializer,
        'retrieve': UserSerializer,
        'partial_update': UserSerializer,
    }

    def get_permissions(self):
        permission_ = self.perms_methods.get(self.action)
        if permission_ is None:
            return super().get_permissions()
        return [permission() for permission in permission_]

    def get_serializer_class(self):
        serializer = self.choice_serializer.get(self.action)
        if serializer is None:
            return super().get_serializer_class()
        return serializer
