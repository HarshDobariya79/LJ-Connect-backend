from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    profile_photo = serializers.SerializerMethodField()

    def get_profile_photo(self, user):
        try:
            google_account = SocialAccount.objects.get(user=user, provider="google")
            return google_account.extra_data.get("picture")
        except SocialAccount.DoesNotExist:
            return None
