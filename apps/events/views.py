from rest_framework import generics
from .models import EventRegistration, Event
from .serializers import EventRegistrationSerializer, EventSerializer


class EventRegistrationCreateView(generics.CreateAPIView):
    """
    POST /api/events/register/
    Accepts registration data for the event.
    """
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
