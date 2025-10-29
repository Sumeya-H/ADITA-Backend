import uuid
from django.db import models
from apps.registrants.models import Registrant
from django.contrib.postgres.fields import JSONField  # or use models.JSONField in Django 3.1+

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
    registrant = models.ForeignKey(
        Registrant, on_delete=models.CASCADE, related_name="event_registrations"
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="registrations"
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    # Core info
    city = models.CharField(max_length=100)
    sub_city = models.CharField(max_length=100, blank=True, null=True)

    university = models.CharField(max_length=255, blank=True, null=True)
    graduation_year = models.CharField(max_length=10, blank=True, null=True)
    fieldOfStudy = models.CharField(max_length=255, blank=True, null=True)

    # Course-related
    selected_course = models.CharField(
        max_length=50, choices=[("none", "None"), ("marketing", "Marketing"), ("ai", "AI")]
    )
    marketing_experience = models.TextField(blank=True, null=True)
    programming_experience = models.CharField(
        max_length=20,
        choices=[("none", "None"), ("basic", "Basic"), ("intermediate", "Intermediate"), ("advanced", "Advanced")],
        default="none", blank=True, null=True
    )
    data_tools = models.CharField(
        max_length=20,
        choices=[("none", "None"), ("excel", "Excel"), ("python", "Python"), ("r", "R"), ("powerbi", "Power BI")],
        default="none", blank=True, null=True
    )
    math_background = models.CharField(
        max_length=20,
        choices=[("none", "None"), ("basic", "Basic"), ("intermediate", "Intermediate"), ("advanced", "Advanced")],
        default="none", blank=True, null=True
    )

    # Familiarity scores (1–5)
    familiarity = models.JSONField(default=dict)  # {"ml": "1", "visualization": "1", "sql": "1"}

    # Common
    motivation = models.TextField(blank=True, null=True)
    referral = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["registrant", "event"], name="unique_event_registration")
        ]

    def __str__(self):
        return f"{self.registrant} -> {self.event.name}"
