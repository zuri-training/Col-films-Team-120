import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


def verify_token(token):
    '''
    This function authenticates user with jwt token
    '''

    if not token:
        raise AuthenticationFailed("Unauthenticated")

    try:
        # Extract payload from token
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Unauthenticated")

    return payload


def is_authenticated(request):
    '''
        Check if user isAuthenticated
    '''

    jwt_token = request.COOKIES.get("user-token")

    payload = verify_token(jwt_token)

    if payload:
        return payload["id"]
    return None
