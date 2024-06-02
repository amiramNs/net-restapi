from rest_framework.serializers import ModelSerializer, Serializer, CharField, IntegerField
from project.apps.profile.models import User


class LoginSerializer(Serializer):
    username = CharField(max_length=150)
    password = CharField(max_length=80)


class TokenSerializer(Serializer):
    access = CharField(max_length=400, required=False, allow_null=True, default=None)
    refresh = CharField(max_length=400, required=False, allow_null=True, default=None)
    token_id = IntegerField(read_only=True)


class LogoutSerializer(Serializer):
    refresh = CharField(max_length=400, required=True)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'job', 'password']


class ResponseUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'job']
