from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permission_classes import IsActiveStaff, IsActiveStudent, IsAdmin
from data.models import StaffDetail

from .serializers import StaffDetailSerializer


class StaffDetailAPI(APIView):
    # authentication_classes = [IsActiveStaff]
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
