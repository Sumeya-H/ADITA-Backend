import uuid
from django.db import models
# or use models.JSONField in Django 3.1+
from django.contrib.postgres.fields import JSONField


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField()
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class EventRegistration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Basic info
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)

    # Location
    city = models.CharField(max_length=100)
    sub_city = models.CharField(max_length=100, blank=True, null=True)

    # Seminar-specific
    organization = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)

    # Extras
    referral = models.CharField(max_length=255, blank=True, null=True)

    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class CustomCourseEnrollment(models.Model):
    EXPERIENCE_CHOICES = [
        ("none", "No experience"),
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    BACKGROUND_CHOICES = [
        ("engineer", "Engineer"),
        ("educator", "Educator"),
        ("healthcare", "Healthcare"),
        ("finance", "Finance"),
        ("it", "IT"),
        ("other", "Other"),
    ]

    REFERRAL_CHOICES = [
        ("social-media", "Social Media"),
        ("friend", "Friend"),
        ("search", "Search Engine"),
        ("event", "Event"),
        ("advertisement", "Advertisement"),
        ("other", "Other"),
    ]

    # ✅ NEW
    MODE_CHOICES = [
        ("online", "Online"),
        ("hybrid", "Hybrid"),
        ("in-person", "In-Person"),
    ]

    # ✅ NEW
    LOCATION_CHOICES = [
        ("aastu", "Addis Ababa Science and Technology University"),
        ("ict-park", "ICT Park"),
        ("fdre-tvt", "FDRE TVT Institute"),
    ]

    program = models.CharField(max_length=255)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)

    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    background = models.CharField(max_length=50, choices=BACKGROUND_CHOICES)
    experience = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES)

    goals = models.TextField(blank=True)
    referral = models.CharField(max_length=50, choices=REFERRAL_CHOICES)

    # ✅ NEW FIELDS
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    location = models.CharField(
        max_length=50,
        choices=LOCATION_CHOICES,
        blank=True,
        null=True
    )

    agreed_terms = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.program}"
