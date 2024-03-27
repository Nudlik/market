from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser

from ads.models import Ad, Comment
from ads.pagination import AdPagination, CommentPagination
from ads.permissions import IsAuthor
from ads.serializers import AdSerializer, CommentSerializer, AdListSerializer
from ads.yasg import ad_doc, comment_doc


class AdViewSet(viewsets.ModelViewSet):
    __doc__ = ad_doc

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = AdPagination
    perms_methods = {
        'list': [AllowAny],
        'update': [IsAuthor | IsAdminUser],
        'partial_update': [IsAuthor | IsAdminUser],
        'destroy': [IsAuthor | IsAdminUser],
    }
    choice_serializer = {
        'list': AdListSerializer,
        'me': AdListSerializer,
    }

    def get_permissions(self):
        self.permission_classes = self.perms_methods.get(self.action, self.permission_classes)
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        return self.choice_serializer.get(self.action, self.serializer_class)

    @action(detail=False, methods=['GET'])
    def me(self, request, *args, **kwargs):
        self.queryset.filter(author=request.user)
        return super().list(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    __doc__ = comment_doc

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    perms_methods = {
        'update': [IsAuthor | IsAdminUser],
        'partial_update': [IsAuthor | IsAdminUser],
        'destroy': [IsAuthor | IsAdminUser],
    }

    def get_permissions(self):
        self.permission_classes = self.perms_methods.get(self.action, self.permission_classes)
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        ad_pk = self.kwargs.get('ad_pk')
        return self.queryset.filter(ad_id=ad_pk)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))
