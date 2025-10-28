from rest_framework.routers import DefaultRouter
from .views import CourseRegistrationViewSet


router = DefaultRouter()
router.register(r'register', CourseRegistrationViewSet, basename='course-registration')

urlpatterns = router.urls
