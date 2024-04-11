from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser

from ads.filters import AdFilerSet
from ads.models import Ad
from ads.paginations import AdPagination

from ads.permissions import IsAuthor
from ads.serializers import AdSerializer, AdListSerializer
from ads.yasg import ad_doc


class AdViewSet(viewsets.ModelViewSet):
    __doc__ = ad_doc

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = AdPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdFilerSet
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
