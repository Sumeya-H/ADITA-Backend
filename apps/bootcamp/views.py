from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BootcampRegistrationSerializer


class BootcampRegistrationCreateView(APIView):
    """
    POST /api/bootcamp/register/

    Accepts multipart/form-data (required for payment_receipt file upload).
    No authentication required — public endpoint.
    """
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = BootcampRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            registration = serializer.save()
            return Response(
                {
                    "message": "Application received successfully.",
                    "registration_id": str(registration.id),
                    "payment_status": registration.payment_status,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
