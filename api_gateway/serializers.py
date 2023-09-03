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


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

    study_resource = serializers.PrimaryKeyRelatedField(
        queryset=StudyResource.objects.all(), required=False, many=True
    )

    batch = serializers.PrimaryKeyRelatedField(
        queryset=Batch.objects.all(), required=False, many=True
    )

    def update(self, instance, validated_data):
        study_resource_data = validated_data.pop("study_resource", None)
        batch_data = validated_data.pop("batch", None)

        instance = super().update(instance, validated_data)

        if study_resource_data is not None:
            instance.study_resource.clear()
            instance.study_resource.add(*study_resource_data)

        if batch_data is not None:
            instance.batch.clear()
            instance.batch.add(*batch_data)

        return instance


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("subject_code", "subject_short_name")
