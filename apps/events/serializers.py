from rest_framework import serializers
from .models import EventRegistration, Event
from apps.registrants.models import Registrant

class EventRegistrationSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    phone = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = EventRegistration
        exclude = ["registered_at", "registrant"]

    def validate(self, data):
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
        return registration

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name", "date", "location"]

