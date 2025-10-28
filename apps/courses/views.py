from rest_framework import viewsets 
from .models import CourseRegistration
from .serializers import CourseRegistrationSerializer

class CourseRegistrationViewSet(viewsets.ModelViewSet):
    queryset = CourseRegistration.objects.all()
    serializer_class = CourseRegistrationSerializer

