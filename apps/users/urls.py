from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views import StudentRegisterAPIView, StaffRegisterAPIView, LoginAPIView


urlpatterns = [
    path('auth/login/', LoginAPIView.as_view(), name='jwt-login'),
    path('students/', StudentRegisterAPIView.as_view(), name='students-register'),
    path('staff/', StaffRegisterAPIView.as_view(), name='staff-register'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
