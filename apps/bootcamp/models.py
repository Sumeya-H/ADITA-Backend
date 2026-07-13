import uuid
from django.db import models


class BootcampRegistration(models.Model):

    # ── Choice constants ──────────────────────────────────────────────────

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("prefer_not_to_say", "Prefer not to say"),
        ("other", "Other"),
    ]

    APPLICANT_TYPE_CHOICES = [
        ("university_student", "University Student"),
        ("recent_graduate", "Recent Graduate"),
        ("high_school_student", "High School Student"),
        ("other", "Other"),
    ]

    ROLE_CHOICES = [
        ("technical", "Technical / Builder"),
        ("non_technical", "Non-Technical / Launcher"),
        ("not_sure", "Not Sure — Let ADITA Assign"),
    ]

    AI_EXPERIENCE_CHOICES = [
        ("yes", "Yes"),
        ("no", "No"),
    ]

    REFERRAL_CHOICES = [
        ("social_media", "Social Media (LinkedIn, Telegram, TikTok, Instagram)"),
        ("friend_classmate", "Friend or Classmate"),
        ("university_notice", "University / Department Notice"),
        ("adita_event", "ADITA Event or Seminar"),
        ("advertisement", "Advertisement"),
        ("other", "Other"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending Review"),
        ("confirmed", "Payment Confirmed"),
        ("rejected", "Payment Rejected"),
        ("refunded", "Refunded"),
    ]

    # ── Primary key ───────────────────────────────────────────────────────

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # ── Section 1: Personal Information ──────────────────────────────────

    full_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    area_of_residence = models.CharField(
        max_length=150,
        help_text="Area or sub-city within Addis Ababa"
    )

    # ── Section 2: Background ─────────────────────────────────────────────

    applicant_type = models.CharField(max_length=30, choices=APPLICANT_TYPE_CHOICES)
    school_university_company = models.CharField(
        max_length=255,
        help_text="Name of school, university, or company"
    )
    field_role = models.CharField(
        max_length=255,
        help_text="Field of study, grade level, or job title depending on applicant type"
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        help_text="Technical/Builder, Non-Technical/Launcher, or Not Sure"
    )

    # ── Section 3: About the Applicant ────────────────────────────────────

    motivation = models.TextField(
        help_text="Why do you want to join Build the Product? (2–3 sentences)"
    )
    ai_experience = models.CharField(
        max_length=5,
        choices=AI_EXPERIENCE_CHOICES,
        help_text="Have you used any AI tools before?"
    )
    ai_tools_used = models.TextField(
        blank=True,
        help_text="Which AI tools? What did you use them for? (leave blank if none)"
    )
    referral = models.CharField(max_length=30, choices=REFERRAL_CHOICES)

    # ── Section 4: Guardian (under-18 only) ───────────────────────────────

    guardian_name = models.CharField(
        max_length=150,
        blank=True,
        help_text="Required for applicants under 18"
    )
    guardian_phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Required for applicants under 18"
    )
    guardian_consent = models.BooleanField(
        default=False,
        help_text="Parent/guardian has approved participation"
    )

    # ── Section 5: Consent & Agreement ───────────────────────────────────

    agreed_terms = models.BooleanField(default=False)
    agreed_photo_consent = models.BooleanField(default=False)
    agreed_data_policy = models.BooleanField(default=False)
    agreed_attendance_commitment = models.BooleanField(default=False)
    agreed_employer_referral = models.BooleanField(
        default=False,
        help_text="Optional — consent for ADITA to share profile with employers"
    )

    # ── Section 6: Payment ────────────────────────────────────────────────

    payment_receipt = models.ImageField(
        upload_to="bootcamp_receipts/",
        help_text="Screenshot or scan of payment receipt"
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending"
    )
    payment_confirmed_at = models.DateTimeField(null=True, blank=True)
    payment_notes = models.TextField(
        blank=True,
        help_text="Internal notes on payment (admin use)"
    )

    # ── Metadata ──────────────────────────────────────────────────────────

    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-registered_at"]
        verbose_name = "Bootcamp Registration"
        verbose_name_plural = "Bootcamp Registrations"

    def __str__(self):
        return f"{self.full_name} — {self.applicant_type} ({self.payment_status})"

    @property
    def is_minor(self):
        """Returns True if applicant was under 18 at time of registration."""
        from datetime import date
        today = date.today()
        age = today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
        return age < 18
