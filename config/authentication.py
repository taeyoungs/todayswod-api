import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from users.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        if token is not None:
            berear, encoded_jwt = token.split(" ")
            decoded_jwt = jwt.decode(
                encoded_jwt, settings.SECRET_KEY, algorithms=["HS256"]
            )
            pk = decoded_jwt.get("pk", None)
            if pk is not None:
                try:
                    user = User.objects.get(pk=pk)
                except User.DoesNotExist:
                    raise exceptions.AuthenticationFailed("No such user")
            else:
                return None
            return (user, None)

        else:
            return None
