from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
