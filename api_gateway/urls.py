from django.urls import path

from .views import (
    BatchAPI,
    BranchAPI,
    BranchCompactAPI,
    DepartmentAPI,
    FacultyAllocationAPI,
    OwnDepartmentAPI,
    StaffDetailAPI,
    StaffDetailCompactAPI,
    StudentDetailAPI,
    StudentDetailCompactAPI,
    SubjectWeightageAPI,
)

urlpatterns = [
    path("v1/staff/", StaffDetailAPI.as_view(), name="staff-list"),
    path(
        "v1/staff/compact/", StaffDetailCompactAPI.as_view(), name="staff-list-compact"
    ),
    path("v1/branch/", BranchAPI.as_view(), name="branch-list"),
    path("v1/branch/compact/", BranchCompactAPI.as_view(), name="branch-compact-list"),
    path("v1/department/", DepartmentAPI.as_view(), name="department-list"),
    path("v1/department/own/", OwnDepartmentAPI.as_view(), name="own-department-list"),
    path("v1/student/", StudentDetailAPI.as_view(), name="student-list"),
    path(
        "v1/student/compact/",
        StudentDetailCompactAPI.as_view(),
        name="student-compact-list",
    ),
    path(
        "v1/faculty-allocation/",
        FacultyAllocationAPI.as_view(),
        name="faculty-allocation-list",
    ),
    path("v1/subject/", SubjectWeightageAPI.as_view(), name="subject-list"),
    path("v1/batch/", BatchAPI.as_view(), name="batch-list"),
]
