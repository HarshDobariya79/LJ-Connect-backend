from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permission_classes import (
    IsActiveStaff,
    IsActiveStudent,
    IsAdmin,
    IsHOD,
)
from data.models import (
    Batch,
    Branch,
    Department,
    FacultyAllocation,
    StaffDetail,
    StudentDetail,
    StudyResource,
    Subject,
    Weightage,
)

from .serializers import (
    BatchSerializer,
    BatchSupportSerializer,
    BranchSerializer,
    BranchSupportSerializer,
    DepartmentSerializer,
    DepartmentSupportSerializer,
    FacultyAllocationSerializer,
    StaffDetailSerializer,
    StaffDetailSupportSerializer,
    StudentDetailSerializer,
    StudentDetailSupportSerializer,
    StudyResourceSerializer,
    SubjectSerializer,
    WeightageSerializer,
)
from .utils import get_email_from_access_token


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


class StudentDetailCompactAPI(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, format=None):
        students = StudentDetail.objects.filter(graduated=False)
        serializer = StudentDetailSupportSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FacultyAllocationAPI(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        allocations = FacultyAllocation.objects.all()
        serializer = FacultyAllocationSerializer(allocations, many=True)
        return Response(serializer.data)

    def post(self, request):
        faculty_id = request.data.get("faculty")
        subject_id = request.data.get("subject")

        if FacultyAllocation.objects.filter(
            faculty_id=faculty_id, subject_id=subject_id
        ).exists():
            return Response(
                {"detail": "Faculty allocation already exists."},
                status=status.HTTP_201_CREATED,
            )

        serializer = FacultyAllocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
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


class SubjectWeightageAPI(APIView):
    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        subject_serializer = SubjectSerializer(data=request.data)
        if subject_serializer.is_valid():
            subject = subject_serializer.save()

            weightages_data = request.data.get("weightage")
            if weightages_data:
                for weightage_item in weightages_data:
                    weightage = Weightage.objects.create(
                        subject=subject, **weightage_item
                    )
                    subject.weightage.add(weightage)

            return Response(subject_serializer.data, status=status.HTTP_201_CREATED)
        return Response(subject_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        subject_code = request.data.get("subject_code")
        try:
            subject = Subject.objects.get(subject_code=subject_code)
        except Subject.DoesNotExist:
            return Response(
                {"detail": "Subject not found."}, status=status.HTTP_404_NOT_FOUND
            )

        subject_serializer = SubjectSerializer(subject, data=request.data)
        if subject_serializer.is_valid():
            subject_serializer.save()

            weightages_data = request.data.get("weightage")
            if weightages_data is not None:
                existing_weightage_ids = [w.id for w in subject.weightage.all()]
                updated_weightage_ids = [w_data.get("id") for w_data in weightages_data]

                for weightage_id in existing_weightage_ids:
                    if weightage_id not in updated_weightage_ids:
                        weightage = Weightage.objects.get(id=weightage_id).delete()

                for weightage_data in weightages_data:
                    weightage_id = weightage_data.get("id")
                    if weightage_id:
                        weightage = Weightage.objects.get(id=weightage_id)
                        for attr, value in weightage_data.items():
                            setattr(weightage, attr, value)
                        weightage.save()
                        subject.weightage.add(weightage)

                    else:
                        weightage = Weightage.objects.create(
                            subject=subject, **weightage_data
                        )
                        subject.weightage.add(weightage)

            return Response(subject_serializer.data, status=status.HTTP_200_OK)
        return Response(subject_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BatchAPI(APIView):
    permission_classes = [IsAdmin | IsHOD]

    def get(self, request):
        email = get_email_from_access_token(request)
        staff_obj = StaffDetail.objects.filter(email=email, admin=True)
        if staff_obj:
            batches = Batch.objects.all()
        else:
            batches = Batch.objects.filter(department__hod__email=email)
        serializer = BatchSerializer(batches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if "faculty" in request.data and not request.data["faculty"]:
            del request.data["faculty"]
        if "student" in request.data and not request.data["student"]:
            del request.data["student"]
        data = request.data.copy()

        faculty_ids = data.pop("faculty", [])
        enrolment_numbers = data.pop("student", [])

        serializer = BatchSerializer(data=data)
        if serializer.is_valid():
            if "department" in request.data:
                department_id = request.data["department"]
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            department = Department.objects.get(id=department_id)
            batch = serializer.save()
            batch.faculty.set(faculty_ids)
            batch.student.set(enrolment_numbers)
            department.batch.add(batch)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        id = request.data.get("id")
        name = request.data.get("name")
        batch = get_object_or_404(Batch, id=id, name=name)
        data = request.data.copy()
        faculty_ids = data.pop("faculty", [])
        enrolment_numbers = data.pop("student", [])

        serializer = BatchSerializer(batch, data=data)
        if serializer.is_valid():
            batch = serializer.save()

            batch.faculty.set(faculty_ids)
            batch.student.set(enrolment_numbers)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OwnDepartmentAPI(APIView):
    permission_classes = [IsAdmin | IsHOD]

    def get(self, request):
        email = get_email_from_access_token(request)
        staff_obj = StaffDetail.objects.filter(email=email, admin=True)
        if staff_obj:
            own_department = Department.objects.filter(locked=False)
        else:
            own_department = Department.objects.filter(hod__email=email, locked=False)
        serializer = DepartmentSupportSerializer(own_department, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BranchCompactAPI(APIView):
    def get(self, request):
        branches = Branch.objects.filter(available=True)
        serializer = BranchSupportSerializer(branches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DepartmentAPI(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if "branch" in request.data and not request.data["branch"]:
            del request.data["branch"]
        data = request.data.copy()

        branches = data.pop("branch", [])

        serializer = DepartmentSerializer(data=data)
        if serializer.is_valid():
            if "batch" in request.data:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            department = serializer.save()
            department.branch.set(branches)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        id = request.data.get("id")
        name = request.data.get("name")
        department = get_object_or_404(Department, id=id, name=name)
        data = request.data.copy()
        branches = data.pop("branch", [])

        serializer = DepartmentSerializer(department, data=data)
        if serializer.is_valid():
            department = serializer.save()

            department.branch.set(branches)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
