from rest_framework import viewsets
from rest_framework.response import Response

from ads.models import Ad, Comment
from ads.pagination import AdPagination
from ads.serializers import AdSerializer, CommentSerializer, AdDetailSerializer


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = AdPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AdDetailSerializer(instance)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
