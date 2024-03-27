from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt import views


class TokenCreateView(views.TokenObtainPairView):
    """
    Принимает набор учетных данных пользователя и возвращает пару веб-токенов доступа и обновления
    JSON для подтверждения аутентификации этих учетных данных.
    """

    @swagger_auto_schema(tags=['token'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenUpdateView(views.TokenRefreshView):
    """
    Принимает веб-токен JSON типа обновления и возвращает веб-токен JSON типа доступа,
    если токен обновления действителен.
    """

    @swagger_auto_schema(tags=['token'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
