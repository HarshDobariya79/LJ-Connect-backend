from django.urls import path

from .views import StaffDetailAPI

urlpatterns = [
    path("v1/staff/", StaffDetailAPI.as_view(), name="staff-list"),
]
