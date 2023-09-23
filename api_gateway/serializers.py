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
    Weightage,
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


class WeightageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weightage
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    weightage = WeightageSerializer(many=True, required=False)  # Set required=False

    class Meta:
        model = Subject
        fields = "__all__"

    def create(self, validated_data):
        weightages_data = validated_data.pop(
            "weightage", []
        )  # Get weightages data or an empty list

        subject = Subject.objects.create(**validated_data)

        for weightage_data in weightages_data:
            Weightage.objects.create(subject=subject, **weightage_data)

        return subject

    def update(self, instance, validated_data):
        weightages_data = validated_data.pop("weightage", [])

        instance.subject_short_name = validated_data.get(
            "subject_short_name", instance.subject_short_name
        )
        instance.subject_full_name = validated_data.get(
            "subject_full_name", instance.subject_full_name
        )
        instance.total_credit = validated_data.get(
            "total_credit", instance.total_credit
        )
        instance.theory_credit = validated_data.get(
            "theory_credit", instance.theory_credit
        )
        instance.tutorial_credit = validated_data.get(
            "tutorial_credit", instance.tutorial_credit
        )
        instance.practical_credit = validated_data.get(
            "practical_credit", instance.practical_credit
        )

        instance.save()

        existing_weightage_ids = [w.id for w in instance.weightage.all()]

        updated_weightage_ids = []
        updated_weightages = []

        for weightage_data in weightages_data:
            weightage_id = weightage_data.get("id")
            if weightage_id:
                updated_weightage_ids.append(weightage_id)
                updated_weightages.append(weightage_data)

        for weightage_id in existing_weightage_ids:
            if weightage_id not in updated_weightage_ids:
                Weightage.objects.get(id=weightage_id).delete()

        for weightage_data in updated_weightages:
            weightage_id = weightage_data.get("id")
            if weightage_id:
                weightage = Weightage.objects.get(id=weightage_id)
                for attr, value in weightage_data.items():
                    setattr(weightage, attr, value)
                weightage.save()
            else:
                Weightage.objects.create(subject=instance, **weightage_data)

        return instance


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
