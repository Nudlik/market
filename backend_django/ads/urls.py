from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ads.views import AdViewSet, CommentViewSet

router = DefaultRouter()
router.register('ads', AdViewSet, basename='ads')
router.register('ads/(?P<ad_pk>[^/.]+)/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
]
