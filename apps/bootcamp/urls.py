from django.urls import path
from .views import BootcampRegistrationCreateView

urlpatterns = [
    path("register/", BootcampRegistrationCreateView.as_view(), name="bootcamp-register"),
]
