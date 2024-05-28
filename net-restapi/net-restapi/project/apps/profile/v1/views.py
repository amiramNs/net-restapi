from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied, AuthenticationFailed, ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView as BaseTokenRefreshView


from project.apps.profile.v1.serializers import (UserSerializer, ResponseUserSerializer, LoginSerializer,
                                                 TokenSerializer, LogoutSerializer)
from project.apps.profile.v1.utils import set_auth_cookie
from project.apps.profile.models import User


@extend_schema(
    tags=['profile'],
    request=LoginSerializer,
    responses={200: OpenApiResponse(response=TokenSerializer, description='SUCCESS'),
               400: OpenApiResponse(description='BAD REQUEST'),
               },
    description="login.",
)
class LoginView(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = LoginSerializer

    @set_auth_cookie
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.authorize_user(serializer)
        token = self.create_token(user)
        return Response(data=token, status=status.HTTP_200_OK)

    def authorize_user(self, serializer):
        try:
            user = User.objects.get(username=serializer.validated_data['username'])
            if user.password == serializer.validated_data['password']:
                return user
        except User.DoesNotExist:
            pass
        raise PermissionDenied()

    def create_token(self, user):
        refresh = RefreshToken.for_user(user)
        token = OutstandingToken.objects.get(token=refresh)
        return {'refresh': str(refresh), 'access': str(refresh.access_token), 'token_id': token.id}


@extend_schema(
    tags=['profile'],
    request=UserSerializer,
    responses={200: OpenApiResponse(response=ResponseUserSerializer, description='SUCCESS'),
               400: OpenApiResponse(description='BAD REQUEST'),
               },
    description="Create Personnel.",
)
class CreateUserViews(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer
    res_serializer = ResponseUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=self.res_serializer(serializer.data).data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['profile'],
    responses={200: OpenApiResponse(response=ResponseUserSerializer, description='SUCCESS'),
               401: OpenApiResponse(description='UNAUTHORIZED'),
               404: OpenApiResponse(description='NOT FOUND')},
    description="Get Personnel.",
)
class GetUserView(APIView):
    serializer_class = ResponseUserSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        obj = self.get_user()
        if obj.id != request.user.id:
            raise ValidationError('Invalid request!')
        serializer = self.serializer_class(instance=obj)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_user(self):
        try:
            return User.objects.get(id=self.kwargs[self.lookup_field])
        except User.DoesNotExist:
            raise NotFound("User NotFound!")


@extend_schema(
    tags=['profile'],
    responses={200: OpenApiResponse(description='SUCCESS'),
               401: OpenApiResponse(description='UNAUTHORIZED'),
               404: OpenApiResponse(description='NOT FOUND')},
    description="logout Personnel.",
)
class LogoutView(APIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.__class__.delete_token(request, raise_exception=True)
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def delete_token(request, raise_exception=True):
        try:
            with transaction.atomic():
                token = RefreshToken(request.data["refresh"])
                token.blacklist()
            return True
        except TokenError as e:
            if raise_exception:
                raise AuthenticationFailed()
            return False


@extend_schema(
    tags=['profile'],
    responses={200: OpenApiResponse(description='SUCCESS'),
               401: OpenApiResponse(description='UNAUTHORIZED'),
               404: OpenApiResponse(description='NOT FOUND')},
    description="Create new access token from given refresh token for requested user.",
)
class TokenRefreshView(BaseTokenRefreshView):
    authentication_classes = ()

    @set_auth_cookie
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = OutstandingToken.objects.get(jti=RefreshToken(request.data['refresh'])['jti'])
        response.data.update({"token_id": token.id})
        return response



