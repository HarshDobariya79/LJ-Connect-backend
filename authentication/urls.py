from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import GoogleLoginView, ProfileView

urlpatterns = [
    # path('accounts/', include('allauth.urls')),
    # path('accounts/social/', include('allauth.socialaccount.urls')),
    path("v1/google/login/", GoogleLoginView.as_view(), name="google_login"),
    path("v1/refresh-token/", TokenRefreshView.as_view(), name="token_refresh"),
    path("v1/profile/", ProfileView.as_view(), name="profile"),
]
