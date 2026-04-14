from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import EnrollmentSerializer, EventRegistrationSerializer, EventRegistrationRetrieveSerializer
from .models import EventRegistration


class EventRegistrationRetrieveView(generics.RetrieveAPIView):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationRetrieveSerializer
    lookup_field = "id"


class EventRegistrationListCreateView(generics.ListCreateAPIView):
    queryset = EventRegistration.objects.all().order_by("-registered_at")
    serializer_class = EventRegistrationSerializer


class EnrollmentCreateView(APIView):
    def post(self, request):
        serializer = EnrollmentSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            enrollment = serializer.save()
            return Response(
                {
                    "message": "Enrollment successful",
                    "enrollment_id": enrollment.id,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmAttendanceView(APIView):
    def post(self, request):
        registration_id = request.data.get("registration_id")
        attendance_type = request.data.get("attendance_type")

        if not registration_id:
            return Response(
                {"error": "registration_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if attendance_type not in ["in_person", "virtual"]:
            return Response(
                {"error": "attendance_type must be 'in_person' or 'virtual'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            registration = EventRegistration.objects.get(id=registration_id)

            if registration.attendance_type:
                return Response(
                    {"message": "Attendance already confirmed"},
                    status=status.HTTP_200_OK
                )

            registration.attendance_type = attendance_type
            registration.save()

            return Response(
                {
                    "message": "Attendance confirmed successfully",
                    "attendance_type": attendance_type
                },
                status=status.HTTP_200_OK
            )

        except EventRegistration.DoesNotExist:
            return Response(
                {"error": "Invalid or expired registration link"},
                status=status.HTTP_404_NOT_FOUND
            )
