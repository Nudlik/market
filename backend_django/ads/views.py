from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from ads.models import Ad, Comment
from ads.pagination import AdPagination
from ads.permissions import EmailOwner
from ads.serializers import AdSerializer, CommentSerializer, AdDetailSerializer


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = AdPagination
    perms_methods = {
        'list': [AllowAny],
        'update': [EmailOwner | IsAdminUser],
        'partial_update': [EmailOwner | IsAdminUser],
        'destroy': [EmailOwner | IsAdminUser],
    }

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AdDetailSerializer(instance)
        return Response(serializer.data)

    def get_permissions(self):
        self.permission_classes = self.perms_methods.get(self.action, self.permission_classes)
        return [permission() for permission in self.permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    perms_methods = {
        'update': [EmailOwner | IsAdminUser],
        'partial_update': [EmailOwner | IsAdminUser],
        'destroy': [EmailOwner | IsAdminUser],
    }

    def get_permissions(self):
        self.permission_classes = self.perms_methods.get(self.action, self.permission_classes)
        return [permission() for permission in self.permission_classes]
