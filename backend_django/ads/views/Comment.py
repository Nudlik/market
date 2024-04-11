from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser

from ads.models import Comment
from ads.paginations import CommentPagination

from ads.permissions import IsAuthor
from ads.serializers import CommentSerializer
from ads.yasg import comment_doc


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
