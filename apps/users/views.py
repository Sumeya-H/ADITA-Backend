import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer, StaffCreateSerializer, StudentCreateSerializer
from rest_framework.permissions import IsAuthenticated


# ----------------------
# Login API
# ----------------------
class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        moodle_token = None
        print(user.username)
        try:
            moodle_response = requests.post(
                "http://localhost/login/token.php",
                data={
                    "username": user.username,     # or Moodle username
                    "password": request.data.get("password"),
                    "service": "test",
                },
                timeout=5
            )

            if moodle_response.status_code == 200:
                moodle_data = moodle_response.json()
                moodle_token = moodle_data.get("token")
                print(moodle_data)

        except requests.RequestException:
            moodle_token = None

        data = {
            'refresh': serializer.validated_data['refresh'],
            'access': serializer.validated_data['access'],
            'moodle_token': moodle_token,
            'user': {
                'id': str(user.id),
                'email': user.email,
                'phone_number': user.phone_number,
                'is_staff': user.is_staff,
                'is_student': hasattr(user, 'student_profile'),
            }
        }

        if hasattr(user, 'staff_profile'):
            data['user']['staff_role'] = user.staff_profile.role
        if hasattr(user, 'student_profile'):
            data['user']['country'] = user.student_profile.country
            data['user']['professional_background'] = user.student_profile.professional_background

        return Response(data, status=status.HTTP_200_OK)


# ----------------------
# Staff Registration API
# ----------------------
class StaffRegisterAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Only admin can create staff

    def post(self, request):
        serializer = StaffCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        staff = serializer.save()
        return Response({
            'id': str(staff.user.id),
            'email': staff.user.email,
            'role': staff.role,
            'department': staff.department,
            'job_title': staff.job_title
        }, status=status.HTTP_201_CREATED)


# ----------------------
# Student Registration API
# ----------------------
class StudentRegisterAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = StudentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        return Response({
            'id': str(student.user.id),
            'email': student.user.email,
            'professional_background': student.professional_background,
            'country': student.country
        }, status=status.HTTP_201_CREATED)
