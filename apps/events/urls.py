from django.urls import path
from .views import EventRegistrationListCreateView, EnrollmentCreateView, EventRegistrationRetrieveView, ConfirmAttendanceView

urlpatterns = [
    path("enrollments/", EnrollmentCreateView.as_view(),
         name="enrollment-create"),
    path("registrations/", EventRegistrationListCreateView.as_view(),
         name="registrations"),
    path("registration/<uuid:uuid>/",
         EventRegistrationRetrieveView.as_view(), name="registration-detail"),
    path("confirm-attendance/", ConfirmAttendanceView.as_view(),
         name="confirm-attendance"),
]
