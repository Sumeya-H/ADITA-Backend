# courses/serializers.py
from django.utils import timezone
from rest_framework import serializers
from .models import CourseRegistration
from .models import Course
from apps.users.serializers import StudentReadSerializer, StaffCreateSerializer


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'code',
            'description',
            'price',
        ]


class CourseRegistrationListSerializer(serializers.ModelSerializer):
    student = StudentReadSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    finance_approved_by = StaffCreateSerializer(read_only=True)

    class Meta:
        model = CourseRegistration
        fields = ["id", "student", "course",
                  "receipt_image", "finance_approved_by", "status"]


class CourseRegistrationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRegistration
        fields = ["course", "receipt_image"]

    def create(self, validated_data):
        student = self.context["request"].user.student_profile
        validated_data.pop("student", None)
        return CourseRegistration.objects.create(
            student=student,
            **validated_data
        )


class FinanceApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRegistration
        fields = []

    def update(self, instance, validated_data):
        staff = self.context["request"].user.staff_profile
        instance.status = CourseRegistration.FINANCE_APPROVED
        instance.finance_approved_by = staff
        instance.finance_approved_at = timezone.now()
        instance.save()
        return instance


class ManagementApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRegistration
        fields = []

    def update(self, instance, validated_data):
        staff = self.context["request"].user.staff_profile
        instance.status = CourseRegistration.MANAGEMENT_APPROVED
        instance.management_approved_by = staff
        instance.management_approved_at = timezone.now()
        instance.save()
        return instance
