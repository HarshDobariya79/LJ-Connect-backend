from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permission_classes import (IsActiveStaff, IsActiveStudent,
                                               IsAdmin)
from data.models import StaffDetail

from .serializers import StaffDetailSerializer


class StaffDetailAPI(APIView):
    # authentication_classes = [IsActiveStaff]
    permission_classes = [IsAdmin]

    def post(self, request):
        staff_details = StaffDetail.objects.all()
        serializer = StaffDetailSerializer(staff_details, many=True)
        return Response(serializer.data)


class StaffDetailAddAPI(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = StaffDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
