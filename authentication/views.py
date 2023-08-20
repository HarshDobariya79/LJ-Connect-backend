from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from decouple import config
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = config("GOOGLE_OAUTH2_CALLBACK_URL")
    client_class = OAuth2Client
