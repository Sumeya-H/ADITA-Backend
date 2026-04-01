from django.contrib import admin
from .models import Course, CourseRegistration

# Register your models here.
admin.site.register(Course)


@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "course",
        "status",
        "prefered_format",
        "moodle_enrolled",
        "finance_approved_by",
        "management_approved_by",
        "created_at",
    )

    list_filter = (
        "status",
        "prefered_format",
        "moodle_enrolled",
        "course",  # ✅ filter by course
        "created_at",
        "finance_approved_at",
        "management_approved_at",
    )

    search_fields = (
        "student__user__username",   # adjust depending on your Student model
        "student__user__email",
        "course__name",
        "course__code",
    )

    autocomplete_fields = ("student", "course")

    readonly_fields = (
        "created_at",
        "finance_approved_at",
        "management_approved_at",
    )

    ordering = ("-created_at",)
