from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permission_classes import (IsActiveStaff, IsActiveStudent,
                                               IsAdmin)
from data.models import StaffDetail

from .serializers import StaffDetailSerializer


class StaffDetailAPI(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        staff_details = StaffDetail.objects.all()
        serializer = StaffDetailSerializer(staff_details, many=True)
        return Response(serializer.data)
