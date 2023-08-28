from django.urls import path

from .views import StaffDetailAddAPI, StaffDetailAPI

urlpatterns = [
    path("v1/staff/", StaffDetailAPI.as_view(), name="staff-list"),
    path("v1/staff/add/", StaffDetailAddAPI.as_view(), name="staff-list-add"),
]
