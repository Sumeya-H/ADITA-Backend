from django.urls import path
from .views import EnrollmentCreateView

urlpatterns = [
    # path("register/", EventRegistrationCreateView.as_view(), name="event-register"),
    # path("list/", EventListView.as_view(), name="event-list"),
    path("enrollments/", EnrollmentCreateView.as_view(),
         name="enrollment-create"),
]
