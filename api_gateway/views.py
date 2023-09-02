from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permission_classes import IsActiveStaff, IsActiveStudent, IsAdmin

from data.models import Branch, FacultyAllocation, StaffDetail, StudentDetail

from .serializers import (
    BranchSerializer,
    BranchSupportSerializer,
    FacultyAllocationSerializer,
    StaffDetailSerializer,
    StaffDetailSupportSerializer
)


class StaffDetailAPI(APIView):
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


class StaffDetailCompactAPI(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        staff_details = StaffDetail.objects.filter(active=True)
        serializer = StaffDetailSupportSerializer(staff_details, many=True)
        return Response(serializer.data)


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

class StudentDetailAPI(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        student_details = StudentDetail.objects.all()
        serializer = StudentDetailSerializer(student_details, many=True)
        serialized_data = serializer.data

        for data in serialized_data:
            branch_code = data["branch"]
            branch_instance = Branch.objects.get(branch_code=branch_code)
            branch_serializer = BranchSupportSerializer(branch_instance)
            data["branch"] = branch_serializer.data

        return Response(serialized_data)

    def post(self, request):
        serializer = StudentDetailSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):

        email = request.data.get("email")

        try:
            student_detail = StudentDetail.objects.get(email=email)
        except StudentDetail.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = StudentDetailSerializer(student_detail, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FacultyAllocationAPI(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        allocations = FacultyAllocation.objects.all()
        serializer = FacultyAllocationSerializer(allocations, many=True)
        return Response(serializer.data)

    def post(self, request):
        faculty_id = request.data.get("faculty")
        subject_id = request.data.get("subject")

        # Check if a FacultyAllocation with the same faculty and subject already exists
        if FacultyAllocation.objects.filter(
            faculty_id=faculty_id, subject_id=subject_id
        ).exists():
            return Response(
                {"detail": "Faculty allocation already exists."},
                status=status.HTTP_201_CREATED,
            )

        serializer = FacultyAllocationSerializer(data=request.data)
        # Assuming you have a unique identifier like 'faculty_id' or 'subject_id'
        object_id = request.data.get("id")
        faculty_id = request.data.get("faculty")
        subject_id = request.data.get("subject")

        try:
            allocation = FacultyAllocation.objects.get(id=object_id)
        except FacultyAllocation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if FacultyAllocation.objects.filter(
            faculty=faculty_id, subject=subject_id
        ).exists():
            allocation.delete()
            return Response(
                {"detail": "Faculty allocation already exists."},
                status=status.HTTP_200_OK,
            )

        serializer = FacultyAllocationSerializer(allocation, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
