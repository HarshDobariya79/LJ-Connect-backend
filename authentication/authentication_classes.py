from rest_framework import permissions, status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

from data.models import StaffDetail, StudentDetail, StudentSemesterRecord


class IsAuthenticatedWithToken(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if auth_header is None:
            return None

        auth_token = auth_header.split(" ")

        if len(auth_token) != 2 or auth_token[0] != "Bearer":
            raise AuthenticationFailed(
                "Invalid authorization header.", code="invalid_auth_header"
            )

        token = auth_token[1]

        try:
            jwt_authentication = JWTAuthentication()
            validated_token = jwt_authentication.get_validated_token(token)

            user = jwt_authentication.get_user(validated_token)

            return (user, None)

        except AuthenticationFailed:
            raise
        return None
