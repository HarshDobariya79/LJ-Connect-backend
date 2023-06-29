from django.urls import path, include
from .views import GoogleLoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("v1/google/login/", GoogleLoginView.as_view(), name="google_login"),
    path('v1/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
]