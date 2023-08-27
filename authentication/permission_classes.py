from rest_framework.permissions import BasePermission

from data.models import StaffDetail, StudentDetail

from .authentication_classes import IsAuthenticatedWithToken


class IsActiveStudent(BasePermission):
    def has_permission(self, request, view):
        user, auth = IsAuthenticatedWithToken().authenticate(request)

        if user and user.is_authenticated:
            student_obj = StudentDetail.objects.filter(
                email=user.email, graduated=False
            )
            return bool(student_obj)

        return False


class IsActiveStaff(BasePermission):
    def has_permission(self, request, view):
        user, auth = IsAuthenticatedWithToken().authenticate(request)

        if user and user.is_authenticated:
            staff_data = StaffDetail.objects.filter(email=user.email, active=True)
            return bool(staff_data)

        return False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user, auth = IsAuthenticatedWithToken().authenticate(request)

        if user and user.is_authenticated:
            staff_data = StaffDetail.objects.filter(email=user.email, admin=True)
            return bool(staff_data)

        return False
