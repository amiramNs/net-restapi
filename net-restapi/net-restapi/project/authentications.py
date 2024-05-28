from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class NetAuthentication(JWTAuthentication):

    def authenticate(self, request):
        header = self.get_header(request)

        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        else:
            raw_token = self.get_raw_token(header)
        if raw_token:
            try:
                validated_token = self.get_validated_token(raw_token)
                user, token = self.get_user(validated_token), validated_token
                return user, token
            except Exception as e:
                raise AuthenticationFailed
        else:
            raise AuthenticationFailed
