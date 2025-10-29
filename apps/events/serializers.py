from rest_framework import serializers
from .models import EventRegistration, Event
from apps.registrants.models import Registrant
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string



class EventRegistrationSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    phone = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = EventRegistration
        exclude = ["registered_at", "registrant"]

    def validate(self, data):

        # --- Check if registrant already exists and is registered ---
        email = data.get("email")
        event_id = data.get("event")
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

        self.send_confirmation_email(registrant.full_name, registrant.email)

        return registration

    def send_confirmation_email(self, registrant_name, recipient_email, program_name="Digital Skills & Emerging Technologies Training Program"):
        subject = "Enrollment Confirmation – Adita Academy"

        # HTML email content
        html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>Enrollment Confirmation</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f7e8cb; margin:0; padding:0;">
      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="padding: 20px 0; background-color:#f7e8cb;">
        <tr>
          <td align="center">
            <table width="600" cellpadding="0" cellspacing="0" border="0" style="background-color:#ffffff; border-radius:8px; padding:40px;">
              <tr>
                <td align="center" style="padding-bottom:20px;">
                  <div style="width:64px; height:64px; background-color:#b25114; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:32px; color:#ffffff;">
                    ✔️
                  </div>
                </td>
              </tr>
              <tr>
                <td align="center" style="font-size:24px; font-weight:bold; color:#6b2e12; padding-bottom:10px;">
                  Enrollment Successful!
                </td>
              </tr>
              <tr>
                <td align="center" style="font-size:16px; color:#6b2e12; padding-bottom:20px;">
                  Hi {registrant_name},<br>
                  Thank you for enrolling in the <strong>{program_name}</strong>. Your enrollment has been confirmed.
                </td>
              </tr>
              <tr>
                <td style="background-color:#f7e8cb; border-radius:8px; padding:20px;">
                  <h3 style="font-size:18px; font-weight:600; color:#6b2e12; margin-top:0;">Next Steps:</h3>
                  <ul style="list-style:none; padding-left:0; margin:0; font-size:16px; color:#6b2e12;">
                    <li style="margin-bottom:10px;">✔️ Check your email for enrollment confirmation and program details</li>
                    <li style="margin-bottom:10px;">✔️ Join the orientation session (details will be emailed)</li>
                  </ul>
                </td>
              </tr>
              <tr>
                <td align="center" style="padding-top:30px; font-size:14px; color:#b25114;">
                  © 2025 Adita Academy. All rights reserved.
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
        """

        # Optional plain text fallback
        text_content = f"Hi {registrant_name},\n\nThank you for enrolling in {program_name}. Your enrollment has been confirmed.\n\nNext steps:\n- Check your email for enrollment confirmation and program details\n- Join the orientation session (details will be emailed)\n\n© 2025 Adita Academy"

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name", "date", "location"]

