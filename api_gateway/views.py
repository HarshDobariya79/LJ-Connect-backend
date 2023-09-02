from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permission_classes import IsActiveStaff, IsActiveStudent, IsAdmin
from data.models import (
    Batch,
    Branch,
    Department,
    StaffDetail,
    StudentDetail,
    StudyResource,
)

from .serializers import (
    BranchSerializer,
    BranchSupportSerializer,
    DepartmentSerializer,
    StaffDetailSerializer,
    StaffDetailSupportSerializer,
)


class StaffDetailAPI(APIView):
    # authentication_classes = [IsActiveStaff]
    permission_classes = [IsAdmin]

    def get(self, request):
        staff_details = StaffDetail.objects.all()
        serializer = StaffDetailSerializer(staff_details, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StaffDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        email = request.data.get("email")

        try:
            staff_detail = StaffDetail.objects.get(email=email)
        except StaffDetail.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = StaffDetailSerializer(staff_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BranchAPI(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        branches = Branch.objects.all()
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        branch_code = request.data.get("branch_code")

        try:
            branch = Branch.objects.get(branch_code=branch_code)
        except Branch.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BranchSerializer(branch, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentAPI(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)

        serialized_data = serializer.data

        for department_data in serialized_data:
            branch_codes = department_data["branch"]
            branch_data_list = []

            for branch_code in branch_codes:
                branch_instance = get_object_or_404(Branch, branch_code=branch_code)
                branch_serializer = BranchSupportSerializer(branch_instance)
                branch_data_list.append(branch_serializer.data)
                department_data["branch"] = branch_data_list

                hod = department_data["hod"]
                hod_instance = StaffDetail.objects.get(email=hod)
                staff_serializer = StaffDetailSupportSerializer(hod_instance)
                department_data["hod"] = staff_serializer.data

        return Response(serialized_data)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        year = request.data.get("year")
        semester = request.data.get("semester")
        department_name = request.data.get("name")

        if year and semester and department_name:
            matching_departments = Department.objects.filter(
                year=year, semester=semester, name=department_name
            )

            if matching_departments.exists():
                try:
                    department = Department.objects.get(
                        year=year, semester=semester, name=department_name
                    )
                except Department.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                serializer = DepartmentSerializer(department, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    "No matching departments found.", status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                "Invalid or missing data in the request.",
                status=status.HTTP_400_BAD_REQUEST,
            )
