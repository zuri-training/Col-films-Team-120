import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


def authenticate_user(token):
    if not token:
        raise AuthenticationFailed("Unauthenticated")

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Unauthenticated")

    return payload
