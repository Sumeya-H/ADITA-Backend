# courses/models.py
import uuid
from django.db import models


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    moodle_course_id = models.PositiveIntegerField(
        help_text="ID of the course in Moodle"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CourseRegistration(models.Model):
    PENDING = "pending"
    FINANCE_APPROVED = "finance_approved"
    MANAGEMENT_APPROVED = "management_approved"
    REJECTED = "rejected"
    ENROLLED = "enrolled"
    ONLINE = "online"
    INPERSON = "inperson"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (FINANCE_APPROVED, "Finance Approved"),
        (MANAGEMENT_APPROVED, "Management Approved"),
        (REJECTED, "Rejected"),
        (ENROLLED, "Enrolled in Moodle"),
    ]

    FORMAT_CHOICES = [
        (ONLINE, "online"),
        (INPERSON, "inperson"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        "users.Student",
        on_delete=models.CASCADE,
        related_name="course_registrations"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="registrations"
    )

    receipt_image = models.ImageField(
        upload_to="receipts/",
        help_text="Payment receipt image"
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=PENDING
    )
    prefered_format = models.CharField(
        max_length=30,
        choices=FORMAT_CHOICES,
        default=ONLINE
    )
    prefered_start_date = models.DateTimeField(null=True, blank=True)

    finance_approved_by = models.ForeignKey(
        "users.Staff",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="finance_approvals"
    )

    management_approved_by = models.ForeignKey(
        "users.Staff",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="management_approvals"
    )

    finance_approved_at = models.DateTimeField(null=True, blank=True)
    management_approved_at = models.DateTimeField(null=True, blank=True)

    moodle_enrolled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student} → {self.course} ({self.status})"
