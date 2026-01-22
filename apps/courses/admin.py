from django.contrib import admin
from .models import Course, CourseRegistration

# Register your models here.
admin.site.register(Course)
admin.site.register(CourseRegistration)
