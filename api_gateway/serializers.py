from rest_framework import serializers

from data.models import (
    Batch,
    Branch,
    Department,
    FacultyAllocation,
    StaffDetail,
    StudentDetail,
    StudyResource,
    Subject,
)


class StaffDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffDetail
        fields = "__all__"


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"


class BranchSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ("branch_code", "branch_short_name")


class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDetail
        fields = "__all__"


class StudentDetailSupportSerializer(serializers.ModelSerializer):
    branch_short_name = serializers.CharField(source="branch.branch_short_name")

    class Meta:
        model = StudentDetail
        fields = (
            "enrolment_no",
            "first_name",
            "middle_name",
            "last_name",
            "branch_short_name",
        )


class FacultyAllocationSerializer(serializers.ModelSerializer):
    faculty_short_name = serializers.CharField(
        source="faculty.short_name", read_only=True
    )
    faculty_first_name = serializers.CharField(
        source="faculty.first_name", read_only=True
    )
    faculty_middle_name = serializers.CharField(
        source="faculty.middle_name", read_only=True
    )
    faculty_last_name = serializers.CharField(
        source="faculty.last_name", read_only=True
    )
    subject_short_name = serializers.CharField(
        source="subject.subject_short_name", read_only=True
    )

    class Meta:
        model = FacultyAllocation
        fields = (
            "id",
            "subject",
            "subject_short_name",
            "faculty",
            "faculty_short_name",
            "faculty_short_name",
            "faculty_first_name",
            "faculty_middle_name",
            "faculty_last_name",
        )


class StaffDetailSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffDetail
        fields = ("email", "first_name", "middle_name", "last_name")


class BatchSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ("id", "name")


class StudyResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyResource
        fields = "__all__"


class DepartmentSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("id", "name", "year", "semester")


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("subject_code", "subject_short_name")


class BatchSerializer(serializers.ModelSerializer):
    faculty = FacultyAllocationSerializer(many=True, required=False)
    student = StudentDetailSupportSerializer(many=True, required=False)
    department = serializers.SerializerMethodField()

    class Meta:
        model = Batch
        fields = (
            "id",
            "name",
            "faculty",
            "student",
            "department",
        )

    def get_department(self, obj):
        departments = obj.department_set.all()
        if departments:
            return {
                "id": departments[0].id,
                "name": departments[0].name,
                "year": departments[0].year,
                "semester": departments[0].semester,
            }
        else:
            return None


class DepartmentSerializer(serializers.ModelSerializer):
    batch = BatchSupportSerializer(many=True, required=False)
    branch = BranchSupportSerializer(many=True, required=False)
    hod_data = StaffDetailSupportSerializer(source="hod", many=False, required=False)

    class Meta:
        model = Department
        fields = (
            "id",
            "year",
            "semester",
            "name",
            "batch",
            "branch",
            "hod",
            "hod_data",
            "locked",
        )
