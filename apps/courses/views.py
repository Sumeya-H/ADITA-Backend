from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from .models import CourseRegistration, Course
from .serializers import (
    CourseRegistrationCreateSerializer,
    FinanceApprovalSerializer,
    ManagementApprovalSerializer,
    CourseSerializer,
    CourseRegistrationListSerializer
)
from .permissions import IsFinanceStaff, IsManagementStaff
from .services.enrollment import enroll_student


class CourseRegistrationCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseRegistrationCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student_profile,
                        status=CourseRegistration.PENDING)


class FinanceApproveAPIView(generics.UpdateAPIView):
    queryset = CourseRegistration.objects.filter(
        status=CourseRegistration.PENDING
    )
    serializer_class = FinanceApprovalSerializer
    permission_classes = [IsFinanceStaff]


class ManagementApproveAPIView(generics.UpdateAPIView):
    queryset = CourseRegistration.objects.filter(
        status=CourseRegistration.FINANCE_APPROVED
    )
    serializer_class = ManagementApprovalSerializer
    permission_classes = [IsManagementStaff]

    def perform_update(self, serializer):
        registration = serializer.save()

        student = registration.student

        # Enroll in Moodle
        enroll_student(
            moodle_token=settings.MOODLE_ADMIN_TOKEN,
            moodle_user_id=student.moodle_user_id,
            moodle_course_id=registration.course.moodle_course_id
        )

        registration.status = CourseRegistration.ENROLLED
        registration.save()


class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]


class CourseRegistrationFinanceListAPIView(generics.ListAPIView):
    serializer_class = CourseRegistrationListSerializer
    permission_classes = [IsFinanceStaff]

    def get_queryset(self):
        return CourseRegistration.objects.filter(
            status=CourseRegistration.PENDING
        )


class CourseRegistrationManagementListAPIView(generics.ListAPIView):
    serializer_class = CourseRegistrationListSerializer
    permission_classes = [IsManagementStaff]

    def get_queryset(self):
        return CourseRegistration.objects.filter(
            status=CourseRegistration.FINANCE_APPROVED
        )
