from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers


class UserRegistrationSerializer(BaseUserRegistrationSerializer):

    class Meta:
        model = get_user_model()
        fields = '__all__'


class CurrentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = '__all__'
