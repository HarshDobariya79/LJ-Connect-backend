from rest_framework import serializers

from data.models import Batch, Branch, Department, StaffDetail, StudyResource


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


class StaffDetailSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffDetail
        fields = ("email", "first_name", "middle_name", "last_name")


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
