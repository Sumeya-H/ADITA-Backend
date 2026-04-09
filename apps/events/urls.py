from django.urls import path
from .views import EventRegistrationListCreateView, EnrollmentCreateView

urlpatterns = [
    path("enrollments/", EnrollmentCreateView.as_view(),
         name="enrollment-create"),
    path("registrations/", EventRegistrationListCreateView.as_view(),
         name="registrations"),
]
