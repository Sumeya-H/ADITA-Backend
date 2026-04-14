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


class EventRegistrationRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ["id", "full_name", "email", "attendance_type"]


def send_course_confirmation_email(self, registrant_name, recipient_email, program_name="Introduction to Artificial Intelligence Course"):
    subject = f"Course Enrollment Confirmation – {program_name}"

    # HTML email content with inline styles and background image
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>Course Enrollment Confirmation</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333333; padding: 20px;">
      <table style="width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; padding: 30px;">
        <tr>
          <td style="background-image: url('https://aditacademy.co/images/courses/introduction-to-artificial-intelligence.webp'); background-size: cover; background-position: center; color: white; padding: 60px 20px; text-align: center; border-radius: 8px 8px 0 0; position: relative;">
            <!-- Overlay to ensure readability -->
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.5); border-radius: 8px 8px 0 0;"></div>
            <h2 style="font-size: 28px; font-weight: bold; z-index: 1; position: relative;">{program_name}</h2>
            <p style="font-size: 18px; z-index: 1; position: relative;">Enrollment Confirmation</p>
          </td>
        </tr>
        <tr>
          <td>
            <p style="font-size: 16px; color: #666666;">Dear <strong>{registrant_name},</strong></p>
            <p style="font-size: 16px; color: #666666;">We are pleased to inform you that your registration for the <strong>{program_name}</strong> has been successfully received.</p>

            <div style="margin-top: 20px;">
              <h3 style="font-size: 18px; font-weight: 600; color: #333333;">Course Details:</h3>
              <p style="font-size: 16px; color: #666666;"><strong>Duration:</strong> 4 weeks, with 8 hours of training per week.</p>
              <p style="font-size: 16px; color: #666666;"><strong>Start Date:</strong> <span style="font-weight: bold; color: #0066cc;">Thursday, February 19</span></p>
              <p style="font-size: 16px; color: #666666;"><strong>Location:</strong> <a href="https://maps.app.goo.gl/9wSnR8WJaHSmFYeH7" style="color: #0066cc;" target="_blank">Federal Technical and Vocational Training Institute (FTVTI)</a> (In-person classes).</p>
              <p style="font-size: 16px; color: #666666;"><strong>For Online Classes:</strong> You will be provided with the LMS link prior to the start date.</p>
            </div>

            <div style="margin-top: 20px;">
              <h3 style="font-size: 18px; font-weight: 600; color: #333333;">Payment Details:</h3>
              <ul style="font-size: 16px; color: #666666; padding-left: 20px;">
                <li><strong>Original Course Fee:</strong> <span style="font-weight: bold; color: #0066cc;">10,000 Birr</span></li>
                <li><strong>Promotional Discount:</strong> <span style="font-weight: bold; color: #0066cc;">25%</span></li>
                <li><strong>Final Discounted Price:</strong> <span style="font-weight: bold; color: #0066cc;">7,500 Birr</span></li>
                <li><strong>Bank:</strong> Bank of Abyssinia</li>
                <li><strong>Account Name:</strong> AFIRICAN DIGITAL AND INNOVATION TECHNOLOGY ACADEMY</li>
                <li><strong>Account Number:</strong> 229456048</li>
              </ul>
              <p style="font-size: 16px; color: #666666;">After making the payment, kindly send a payment screenshot to our Telegram account: <a href="https://t.me/adit_academy?direct" style="color: #0066cc;" target="_blank">@adit_academy</a></p>
            </div>

            <a href="https://t.me/adit_academy?direct" style="display: inline-block; background-color: #0066cc; color: #ffffff; font-size: 16px; font-weight: bold; padding: 12px 20px; border-radius: 5px; text-align: center; text-decoration: none; margin-top: 20px;" target="_blank">Confirm Payment</a>

            <div style="font-size: 14px; text-align: center; color: #999999; margin-top: 20px;">
              <p>© 2025 Adita Academy. All rights reserved.</p>
            </div>
          </td>
        </tr>
      </table>

    </body>
    </html>
    """

    # Optional plain text fallback
    text_content = f"""
    Hi {registrant_name},

    We are pleased to inform you that your registration for the Introduction to Artificial Intelligence course has been successfully received.

    Course Details:
    Duration: 4 weeks, with 8 hours of training per week
    Start Date: Thursday, February 19
    Location: Federal Technical and Vocational Training Institute (FTVTI) (In-person classes)
    For Online Classes: You will be provided with the LMS link prior to the start date.

    Payment Details:
    Original Course Fee: 10,000 Birr
    Promotional Discount: 25%
    Final Discounted Price: 7,500 Birr

    Bank: Bank of Abyssinia
    Account Name: AFIRICAN DIGITAL AND INNOVATION TECHNOLOGY ACADEMY
    Account Number: 229456048

    After making the payment, kindly send a payment screenshot to our Telegram account: @adit_academy

    © 2025 Adita Academy. All rights reserved.
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
