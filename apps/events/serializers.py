from rest_framework import serializers
from .models import EventRegistration, Event
from apps.registrants.models import Registrant
from django.core.mail import send_mail
from uuid import UUID


class EventRegistrationSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    phone = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = EventRegistration
        exclude = ["registered_at", "registrant"]

    def validate(self, data):
        event_id = data.get("event")
        try:
            UUID(str(event_id))
        except (ValueError, TypeError):
            raise serializers.ValidationError({"event": "Invalid event ID"})

        # --- Check if registrant already exists and is registered ---
        email = data.get("email")
        registrant = Registrant.objects.filter(email=email).first()
        if registrant and EventRegistration.objects.filter(registrant=registrant, event_id=event_id).exists():
            raise serializers.ValidationError({"detail": "You have already registered for this event."})

        selected_course = data.get("selected_course")

        if selected_course == "marketing" and not data.get("marketing_experience"):
            raise serializers.ValidationError(
                {"marketing_experience": "This field is required for Marketing course."}
            )

        if selected_course == "ai" and data.get("programming_experience") == "none":
            raise serializers.ValidationError(
                {"programming_experience": "Programming experience is required for AI course."}
            )

        return data

    def create(self, validated_data):
        # Extract registrant info from validated_data
        full_name = validated_data.pop("full_name")
        email = validated_data.pop("email")
        phone = validated_data.pop("phone", "")

        # Either get existing registrant or create a new one
        registrant, created = Registrant.objects.get_or_create(
            email=email,
            defaults={"full_name": full_name, "phone": phone}
        )

        # Create the event registration linked to this registrant
        registration = EventRegistration.objects.create(
            registrant=registrant,
            **validated_data
        )

        self.send_confirmation_email(registrant, event)

        return registration

    def send_confirmation_email(self, registrant, event):
        subject = f"Confirmation for {event.name}"
        message = (
            f"Hello {registrant.full_name},\n\n"
            f"Thank you for registering for {event.name}!\n\n"
            f"Event Details:\n"
            f"Date: {event.date}\n"
            f"Location: {event.location}\n\n"
            f"We’re excited to have you join us!\n\n"
            f"– The {event.name} Team"
        )

        send_mail(
            subject,
            message,
            from_email=None,  # Uses DEFAULT_FROM_EMAIL
            recipient_list=[registrant.email],
            fail_silently=False,
        )


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name", "date", "location"]

