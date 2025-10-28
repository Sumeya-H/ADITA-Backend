from django.db import models
from apps.registrants.models import Registrant

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField()
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class EventRegistration(models.Model):
    registrant = models.ForeignKey(Registrant, on_delete=models.CASCADE, related_name='event_registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('registrant', 'event')

    def __str__(self):
        return f"{self.registrant.full_name} -> {self.event.name}"

