from django.contrib import admin
from django.utils.html import format_html
from django.contrib.admin import SimpleListFilter
from django.http import HttpResponse
import csv

from .models import CustomCourseEnrollment, EventRegistration


class ModeLocationFilterEventRegistration(SimpleListFilter):
    title = "Mode Type"
    parameter_name = "mode_type"

    def lookups(self, request, model_admin):
        return (
            ("online", "Online Only"),
            ("physical", "In-Person Only"),
        )

    def queryset(self, request, queryset):
        if self.value() == "online":
            return queryset.filter(attendance_type="virtual")
        if self.value() == "physical":
            return queryset.filter(attendance_type="in_person")
        return queryset


class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "attendance_type",
                    "city", "registered_at")
    list_filter = (ModeLocationFilterEventRegistration,
                   "city", "registered_at")


admin.site.register(EventRegistration, EventRegistrationAdmin)


class ModeLocationFilter(SimpleListFilter):
    title = "Mode Type"
    parameter_name = "mode_type"

    def lookups(self, request, model_admin):
        return (
            ("online", "Online Only"),
            ("physical", "Hybrid / In-Person"),
        )

    def queryset(self, request, queryset):
        if self.value() == "online":
            return queryset.filter(mode="online")
        if self.value() == "physical":
            return queryset.filter(mode__in=["hybrid", "in-person"])
        return queryset


class ExperienceLevelFilter(SimpleListFilter):
    title = "Experience Level Group"
    parameter_name = "experience_level"

    def lookups(self, request, model_admin):
        return (
            ("low", "Beginner Level"),
            ("high", "Intermediate+"),
        )

    def queryset(self, request, queryset):
        if self.value() == "low":
            return queryset.filter(experience__in=["none", "beginner"])
        if self.value() == "high":
            return queryset.filter(experience__in=["intermediate", "advanced"])
        return queryset


# ✅ CSV Export Action

def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=enrollments.csv"

    writer = csv.writer(response)
    writer.writerow([
        "Full Name",
        "Email",
        "Phone",
        "Program",
        "Mode",
        "Location",
        "Experience",
        "Background",
        "Referral",
        "Country",
        "City",
        "Created At",
    ])

    for obj in queryset:
        writer.writerow([
            f"{obj.first_name} {obj.last_name}",
            obj.email,
            obj.phone,
            obj.program,
            obj.mode,
            obj.location,
            obj.experience,
            obj.background,
            obj.referral,
            obj.country,
            obj.city,
            obj.created_at,
        ])

    return response


export_to_csv.short_description = "Export selected to CSV"


# ✅ Admin Configuration

@admin.register(CustomCourseEnrollment)
class CustomCourseEnrollmentAdmin(admin.ModelAdmin):

    # 👉 Columns shown in list
    list_display = (
        "full_name",
        "program",
        "email",
        "phone",
        "colored_mode",
        "location",
        "experience",
        "background",
        "referral",
        "country",
        "city",
        "agreed_terms",
        "created_at",
    )

    # 👉 Filters
    list_filter = (
        ModeLocationFilter,
        ExperienceLevelFilter,
        "mode",
        "location",
        "experience",
        "background",
        "referral",
        "country",
        "agreed_terms",
        "created_at",
    )

    # 👉 Search
    search_fields = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "program",
        "city",
        "country",
    )

    # 👉 Read-only fields
    readonly_fields = ("created_at",)

    # 👉 Ordering
    ordering = ("-created_at",)

    # 👉 Pagination
    list_per_page = 25

    # 👉 Actions
    actions = [export_to_csv]

    # ✅ Full name column
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    full_name.short_description = "Full Name"

    # ✅ Colored mode column
    def colored_mode(self, obj):
        colors = {
            "online": "#007bff",      # blue
            "hybrid": "#fd7e14",      # orange
            "in-person": "#28a745",   # green
        }
        return format_html(
            '<strong style="color: {};">{}</strong>',
            colors.get(obj.mode, "#000"),
            obj.mode.capitalize()
        )

    colored_mode.short_description = "Mode"
