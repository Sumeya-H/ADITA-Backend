from django.contrib import admin
from .models import User, Student, Staff

admin.site.register(User)
admin.site.register(Staff)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ("user__username", "user__email")
