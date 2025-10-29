from django.urls import path
from .views import EventRegistrationCreateView, EventListView

urlpatterns = [
    path("register/", EventRegistrationCreateView.as_view(), name="event-register"),
    path("list/", EventListView.as_view(), name="event-list"),
]
