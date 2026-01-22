from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import EnrollmentSerializer


# class EventRegistrationCreateView(generics.CreateAPIView):
#     queryset = EventRegistration.objects.all()
#     serializer_class = EventRegistrationSerializer
#
# class EventListView(generics.ListAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer


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
