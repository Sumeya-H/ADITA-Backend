from rest_framework import serializers
from .models import CustomCourseEnrollment, EventRegistration
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = "__all__"
        read_only_fields = ["id", "registered_at"]

    def validate_email(self, value):
        if EventRegistration.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "This email is already registered.")
        return value

    def create(self, validated_data):
        # Save user first
        instance = super().create(validated_data)

        try:
            send_course_confirmation_email(
                None,
                registrant_name=instance.full_name,
                recipient_email=instance.email,
                registration_id=str(instance.id)
            )
        except Exception as e:
            # Don't break registration if email fails
            print("Email sending failed:", str(e))

        return instance


class EventRegistrationRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ["id", "full_name", "email", "attendance_type"]


def send_course_confirmation_email(self, registrant_name, recipient_email, registration_id):
    subject = f"Confirm your attendance for the AI For Leaders Seminar"

    # HTML email content with inline styles and background image
    html_content = f"""
    <!DOCTYPE html>

    <html>
    <head>
      <meta charset="UTF-8">
      <title>Confirm Your Attendance</title>
    </head>

    <body style="margin:0; padding:0; font-family: Arial, sans-serif; background:#f4f4f4;">

      <table width="100%" cellpadding="0" cellspacing="0" style="padding:20px 0;">
        <tr>
          <td align="center">

        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:10px; overflow:hidden;">

          <!-- Header -->
          <tr>
            <td style="background:#0f172a; padding:20px; text-align:center; color:#ffffff;">
            <div>
              <h2 style="margin:0;">AI For Leaders Seminar</h2>
              </div>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:30px; color:#333333;">

              <h3 style="margin-top:0;">Hello {registrant_name},</h3>

              <p>
                Thank you for registering for the <strong>AI For Leaders Seminar</strong>.
                We are excited to have you join us.
              </p>

              <p>
                To help us prepare properly, please confirm how you will attend the seminar:
              </p>

              <!-- CTA Button -->
              <div style="text-align:center; margin:30px 0;">
                <a href="https://aditacademy.co/attendance-confirmation?registration_id={registration_id}"
                   style="background:#2563eb; color:#ffffff; padding:14px 22px; text-decoration:none; border-radius:6px; font-weight:bold; display:inline-block;">
                  Confirm Your Attendance
                </a>
              </div>

              <p>
                You will be able to choose between:
              </p>

              <ul>
                <li>📍 In-person attendance (venue details will be sent later)</li>
                <li>💻 Virtual attendance (meeting link will be shared before the event)</li>
              </ul>

              <p style="margin-top:25px;">
                This helps us ensure you get the correct access and event information.
              </p>

              <p>
                If you did not register for this event, you can safely ignore this email.
              </p>

              <p style="margin-top:30px;">
                Best regards,<br/>
                <strong>AI For Leaders Team</strong>
              </p>

            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background:#f1f5f9; padding:15px; text-align:center; font-size:12px; color:#666;">
              © 2026 AI For Leaders Seminar. All rights reserved.
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
    text_content = f"""
    Hi {registrant_name},


    Thank you for registering for the AI For Leaders Seminar. We are excited to have you join us.

    To help us prepare properly, please confirm how you will attend the seminar by clicking the link below:

    https://yourdomain.com/attendance-confirmation?registration_id={registration_id}

    Once you open the link, you will be able to choose:
    - In-person attendance (venue details will be sent later)
    - Virtual attendance (meeting link will be shared before the event)

    This helps us ensure you receive the correct event information.

    If you did not register for this event, you can safely ignore this email.

    Best regards,
    AI For Leaders Team

    © 2026 AI For Leaders Seminar. All rights reserved.
    """

    # Sending the email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)


# class EventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = ["id", "name", "date", "location"]


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomCourseEnrollment
        fields = "__all__"

    def validate_agreed_terms(self, value):
        if not value:
            raise serializers.ValidationError(
                "You must agree to the terms and conditions.")
        return value

    def validate_email(self, value):
        # get program from request data
        program = self.initial_data.get("program")

        if CustomCourseEnrollment.objects.filter(
            email=value,
            program=program
        ).exists():
            raise serializers.ValidationError({
                "error": "EMAIL_EXISTS",
                "message": "An enrollment with this email already exists for this program."
            })

        return value

    def validate_phone(self, value):
        if CustomCourseEnrollment.objects.filter(phone=value).exists():
            raise serializers.ValidationError({
                "error": "PHONE_EXISTS",
                "message": "An enrollment with this phone number already exists."

            })
        return value

    def validate(self, data):
        required_fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "country",
            "city",
            "background",
            "experience",
        ]

        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError(
                    {field: "This field is required."})

        return data
