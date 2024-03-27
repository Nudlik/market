from djoser import views
from rest_framework.permissions import AllowAny, IsAdminUser

from ads.permissions import IsAuthor
from users.pagination import UserPagination
from users.serializers import UserSerializer


class UserViewSet(views.UserViewSet):
    pagination_class = UserPagination
    perms_methods = {
        'create': [AllowAny],
        'update': [IsAuthor | IsAdminUser],
        'partial_update': [IsAuthor | IsAdminUser],
        'destroy': [IsAuthor | IsAdminUser],
    }
    choice_serializer = {
        'list': UserSerializer,
        'me': UserSerializer,
        'retrieve': UserSerializer,
    }

    def get_permissions(self):
        self.permission_classes = self.perms_methods.get(self.action, self.permission_classes)
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        return self.choice_serializer.get(self.action, self.serializer_class)
