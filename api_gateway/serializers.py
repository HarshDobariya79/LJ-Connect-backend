from rest_framework import serializers

from data.models import (
    Batch,
    Branch,
    FacultyAllocation,
    StaffDetail,
    StudentDetail,
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
