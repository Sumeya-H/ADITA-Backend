from rest_framework import serializers
from .models import CourseRegistration, Course
from apps.registrants.models import Registrant
from apps.registrants.serializers import RegistrantSerializer


class CourseRegistrationSerializer(serializers.ModelSerializer):
    # no nested serializer here
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    phone = serializers.CharField(write_only=True)
    country = serializers.CharField(write_only=True)
    city = serializers.CharField(write_only=True)
    background = serializers.CharField(write_only=True, required=False, allow_blank=True)
    experience = serializers.CharField(write_only=True, required=False, allow_blank=True)

    registrant = RegistrantSerializer(read_only=True)

    class Meta:
        model = CourseRegistration
        fields = [
            'id', 'course', 'occupation', 'organization', 'experience_years', 'registered_at',
            # registrant info (write-only)
            'first_name', 'last_name', 'email', 'phone', 'country', 'city', 'background', 'experience',
            # output
            'registrant',
        ]

    def create(self, validated_data):
        # Extract registrant info from flat fields
        registrant_fields = {
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'email': validated_data.pop('email'),
            'phone': validated_data.pop('phone'),
            'country': validated_data.pop('country'),
            'city': validated_data.pop('city'),
            'background': validated_data.pop('background', ''),
            'experience': validated_data.pop('experience', ''),
        }

        registrant, _ = Registrant.objects.get_or_create(
            email=registrant_fields['email'],
            defaults=registrant_fields
        )

        registration = CourseRegistration.objects.create(
            registrant=registrant,
            **validated_data
        )
        return registration

