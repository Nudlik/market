from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users import views

router = SimpleRouter()
router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),

    path('token/', views.TokenCreateView.as_view(), name='token-create'),
    path('refresh/', views.TokenUpdateView.as_view(), name='token-refresh'),
]
