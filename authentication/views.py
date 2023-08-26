from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from decouple import config
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from data.models import Department, StaffDetail, StudentDetail

from .authentication_classes import IsAuthenticatedWithToken
from .serializers import UserSerializer


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = config("GOOGLE_OAUTH2_CALLBACK_URL")
    client_class = OAuth2Client


User = get_user_model()


class ProfileView(APIView):
    authentication_classes = [IsAuthenticatedWithToken]

    def post(self, request, format=None):
        if request.user.is_authenticated:
            user = request.user
            serializer = UserSerializer(user)

            email = user.email
            role = None
            print(email)
            if StaffDetail.objects.filter(email=email, admin=True).exists():
                role = "admin"
            elif Department.objects.filter(hod__email=email).exists():
                role = "hod"
            elif StaffDetail.objects.filter(email=email, active=True).exists():
                role = "staff"
            elif StudentDetail.objects.filter(email=email, graduated=False).exists():
                role = "student"

            else:
                role = "guest"

            response_data = {
                **serializer.data,
                "role": role,
            }

            return Response(response_data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
