from django.urls import path
from .views import (
    CourseRegistrationCreateAPIView,
    FinanceApproveAPIView,
    ManagementApproveAPIView,
    CourseListAPIView,
    CourseRegistrationFinanceListAPIView,
    CourseRegistrationManagementListAPIView
)

urlpatterns = [
    path('register/', CourseRegistrationCreateAPIView.as_view(),
         name='course-register'),
    path('register/finance/', CourseRegistrationFinanceListAPIView.as_view(),
         name='course-registeration-finance'),
    path('register/management/', CourseRegistrationManagementListAPIView.as_view(),
         name='course-registeration-management'),
    path('finance-approve/<uuid:pk>/',
         FinanceApproveAPIView.as_view(), name='finance-approve'),
    path('management-approve/<uuid:pk>/',
         ManagementApproveAPIView.as_view(), name='management-approve'),
    path('', CourseListAPIView.as_view(), name='course-list'),
]
