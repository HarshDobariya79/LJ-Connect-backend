from rest_framework import serializers

from data.models import StaffDetail


class StaffDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffDetail
        fields = "__all__"
