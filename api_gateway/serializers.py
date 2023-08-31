from rest_framework import serializers

from data.models import Branch, StaffDetail, StudentDetail


class StaffDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffDetail
        fields = "__all__"


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"


class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDetail
        fields = "__all__"
