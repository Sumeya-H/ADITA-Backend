import csv
from datetime import datetime

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.http import HttpResponse
from django.utils.html import format_html

from .models import BootcampRegistration
from .serializers import send_bootcamp_payment_confirmed_email


# ── Custom filters ────────────────────────────────────────────────────────────

class AgeGroupFilter(SimpleListFilter):
    title = "Age Group"
    parameter_name = "age_group"

    def lookups(self, request, model_admin):
        return (
            ("minor", "Under 18"),
            ("adult", "18 and over"),
        )

    def queryset(self, request, queryset):
        from datetime import date
        today = date.today()
        # 18th birthday cutoff
        cutoff = date(today.year - 18, today.month, today.day)
        if self.value() == "minor":
            return queryset.filter(date_of_birth__gt=cutoff)
        if self.value() == "adult":
            return queryset.filter(date_of_birth__lte=cutoff)
        return queryset


class RoleFilter(SimpleListFilter):
    title = "Role Type"
    parameter_name = "role_type"

    def lookups(self, request, model_admin):
        return (
            ("technical", "Technical / Builder"),
            ("non_technical", "Non-Technical / Launcher"),
            ("not_sure", "Not Sure"),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(role=self.value())
        return queryset


# ── Admin actions ─────────────────────────────────────────────────────────────

def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="bootcamp_registrations_{datetime.now().strftime("%Y%m%d_%H%M")}.csv"'
    )

    writer = csv.writer(response)
    writer.writerow([
        "ID",
        "Full Name",
        "Date of Birth",
        "Gender",
        "Email",
        "Phone",
        "Area of Residence",
        "Applicant Type",
        "School / University / Company",
        "Field / Role / Grade",
        "Role",
        "Motivation",
        "AI Experience",
        "AI Tools Used",
        "Referral",
        "Guardian Name",
        "Guardian Phone",
        "Guardian Consent",
        "Agreed Terms",
        "Photo Consent",
        "Data Policy",
        "Attendance Commitment",
        "Employer Referral Consent",
        "Payment Status",
        "Payment Confirmed At",
        "Registered At",
    ])

    for obj in queryset:
        writer.writerow([
            str(obj.id),
            obj.full_name,
            obj.date_of_birth,
            obj.get_gender_display(),
            obj.email,
            obj.phone,
            obj.area_of_residence,
            obj.get_applicant_type_display(),
            obj.school_university_company,
            obj.field_role,
            obj.get_role_display(),
            obj.motivation,
            obj.get_ai_experience_display(),
            obj.ai_tools_used,
            obj.get_referral_display(),
            obj.guardian_name,
            obj.guardian_phone,
            obj.guardian_consent,
            obj.agreed_terms,
            obj.agreed_photo_consent,
            obj.agreed_data_policy,
            obj.agreed_attendance_commitment,
            obj.agreed_employer_referral,
            obj.get_payment_status_display(),
            obj.payment_confirmed_at or "",
            obj.registered_at,
        ])

    return response

export_to_csv.short_description = "Export selected registrations to CSV"


def confirm_payment_and_notify(modeladmin, request, queryset):
    """
    Mark selected registrations as payment confirmed and send confirmation email.
    Use this after manually verifying the payment receipt.
    """
    from django.utils import timezone

    updated = 0
    for obj in queryset.filter(payment_status="pending"):
        obj.payment_status = "confirmed"
        obj.payment_confirmed_at = timezone.now()
        obj.save()

        try:
            send_bootcamp_payment_confirmed_email(
                full_name=obj.full_name,
                recipient_email=obj.email,
            )
        except Exception as e:
            modeladmin.message_user(
                request,
                f"Payment confirmed for {obj.full_name} but email failed: {e}",
                level="warning",
            )

        updated += 1

    modeladmin.message_user(
        request,
        f"{updated} registration(s) confirmed and notified by email.",
    )

confirm_payment_and_notify.short_description = "Confirm payment & send confirmation email"


def mark_payment_rejected(modeladmin, request, queryset):
    updated = queryset.filter(payment_status="pending").update(payment_status="rejected")
    modeladmin.message_user(request, f"{updated} registration(s) marked as payment rejected.")

mark_payment_rejected.short_description = "Mark payment as rejected"


# ── Admin configuration ───────────────────────────────────────────────────────

@admin.register(BootcampRegistration)
class BootcampRegistrationAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "email",
        "phone",
        "applicant_type",
        "role",
        "colored_payment_status",
        "area_of_residence",
        "registered_at",
    )

    list_filter = (
        "payment_status",
        "applicant_type",
        RoleFilter,
        AgeGroupFilter,
        "gender",
        "referral",
        "ai_experience",
        "agreed_employer_referral",
        "registered_at",
    )

    search_fields = (
        "full_name",
        "email",
        "phone",
        "school_university_company",
        "area_of_residence",
    )

    readonly_fields = (
        "id",
        "registered_at",
        "updated_at",
        "payment_confirmed_at",
        "receipt_preview",
    )

    ordering = ("-registered_at",)
    list_per_page = 25

    actions = [export_to_csv, confirm_payment_and_notify, mark_payment_rejected]

    fieldsets = (
        ("Personal Information", {
            "fields": (
                "id",
                "full_name",
                "date_of_birth",
                "gender",
                "email",
                "phone",
                "area_of_residence",
            )
        }),
        ("Background", {
            "fields": (
                "applicant_type",
                "school_university_company",
                "field_role",
                "role",
            )
        }),
        ("About the Applicant", {
            "fields": (
                "motivation",
                "ai_experience",
                "ai_tools_used",
                "referral",
            )
        }),
        ("Guardian (Under 18 Only)", {
            "classes": ("collapse",),
            "fields": (
                "guardian_name",
                "guardian_phone",
                "guardian_consent",
            )
        }),
        ("Consent & Agreement", {
            "fields": (
                "agreed_terms",
                "agreed_photo_consent",
                "agreed_data_policy",
                "agreed_attendance_commitment",
                "agreed_employer_referral",
            )
        }),
        ("Payment", {
            "fields": (
                "payment_receipt",
                "receipt_preview",
                "payment_status",
                "payment_confirmed_at",
                "payment_notes",
            )
        }),
        ("Metadata", {
            "fields": ("registered_at", "updated_at"),
        }),
    )

    # ── Display helpers ───────────────────────────────────────────────────

    def colored_payment_status(self, obj):
        colors = {
            "pending": "#e6a817",
            "confirmed": "#28a745",
            "rejected": "#dc3545",
            "refunded": "#6c757d",
        }
        labels = {
            "pending": "⏳ Pending",
            "confirmed": "✅ Confirmed",
            "rejected": "❌ Rejected",
            "refunded": "↩ Refunded",
        }
        return format_html(
            '<strong style="color: {};">{}</strong>',
            colors.get(obj.payment_status, "#000"),
            labels.get(obj.payment_status, obj.payment_status),
        )
    colored_payment_status.short_description = "Payment"

    def receipt_preview(self, obj):
        if obj.payment_receipt:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="max-height:200px; border-radius:4px;" />'
                '</a>',
                obj.payment_receipt.url,
                obj.payment_receipt.url,
            )
        return "No receipt uploaded"
    receipt_preview.short_description = "Receipt Preview"
