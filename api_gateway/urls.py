from django.urls import path

from .views import BranchAPI, StaffDetailAPI

urlpatterns = [
    path("v1/staff/", StaffDetailAPI.as_view(), name="staff-list"),
    path("v1/branch/", BranchAPI.as_view(), name="branch-list"),
]
