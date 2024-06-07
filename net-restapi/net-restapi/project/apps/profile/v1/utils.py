from datetime import datetime
from jwt import decode as jwt_decode
from django.conf import settings
from rest_framework import status


def set_auth_cookie(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=response.data.get('access'),
                expires=datetime.fromtimestamp(
                    jwt_decode(response.data.get('access'), verify=True, options={"verify_signature": False})['exp']
                ),
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
        return response

    return wrapper


def clear_auth_cookie(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            response.delete_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            )
        return response

    return wrapper
