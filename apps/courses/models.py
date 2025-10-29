import uuid
from django.db import models
from apps.registrants.models import Registrant

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class CourseRegistration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registrant = models.ForeignKey(Registrant, on_delete=models.CASCADE, related_name='course_registrations')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    experience_years = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('registrant', 'course')

    def __str__(self):
        return f"{self.registrant.full_name} -> {self.course.name}"

