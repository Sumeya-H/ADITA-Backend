from rest_framework import serializers
from .models import CustomCourseEnrollment
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string


# class EventRegistrationSerializer(serializers.ModelSerializer):
#    full_name = serializers.CharField(write_only=True)
#    email = serializers.EmailField(write_only=True)
#    phone = serializers.CharField(write_only=True, required=False, allow_blank=True)
#
#    class Meta:
#        model = EventRegistration
#        exclude = ["registered_at", "registrant"]
#
#    def validate(self, data):
#
#        # --- Check if registrant already exists and is registered ---
#        email = data.get("email")
#        event_id = data.get("event")
#        registrant = Registrant.objects.filter(email=email).first()
#        if registrant and EventRegistration.objects.filter(registrant=registrant, event_id=event_id).exists():
#            raise serializers.ValidationError({"detail": "You have already registered for this event."})
#
#        selected_course = data.get("selected_course")
#
#        if selected_course == "marketing" and not data.get("marketing_experience"):
#            raise serializers.ValidationError(
#                {"marketing_experience": "This field is required for Marketing course."}
#            )
#
#        if selected_course == "ai" and data.get("programming_experience") == "none":
#            raise serializers.ValidationError(
#                {"programming_experience": "Programming experience is required for AI course."}
#            )
#
#        return data
#
#    def create(self, validated_data):
#        # Extract registrant info from validated_data
#        full_name = validated_data.pop("full_name")
#        email = validated_data.pop("email")
#        phone = validated_data.pop("phone", "")
#
#        # Either get existing registrant or create a new one
#        registrant, created = Registrant.objects.get_or_create(
#            email=email,
#            defaults={"full_name": full_name, "phone": phone}
#        )
#
#        # Create the event registration linked to this registrant
#        registration = EventRegistration.objects.create(
#            registrant=registrant,
#            **validated_data
#        )
#
#        self.send_confirmation_email(registrant.full_name, registrant.email)
#
#        return registration


def send_course_confirmation_email(self, registrant_name, recipient_email, program_name="Introduction to Artificial Intelligence Course"):
    subject = f"Course Enrollment Confirmation – {program_name}"

    # HTML email content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>Course Enrollment Confirmation</title>
      <style>
        /* Basic reset for consistent rendering across email clients */
        body, h1, h2, h3, p, ul, li {
          margin: 0;
          padding: 0;
        }
        body {
          font-family: Arial, sans-serif;
          background-color: #f4f4f9; /* Light neutral background */
          color: #333333; /* Dark gray text for better contrast */
          padding: 20px;
        }
        a {
          color: #0066cc; /* Soft blue for links */
          text-decoration: none;
        }
        table {
          width: 100%;
          max-width: 600px;
          margin: 0 auto;
          background-color: #ffffff; /* White background for the content */
          border-radius: 8px;
          padding: 30px;
        }
        h1, h2, h3 {
          color: #333333; /* Dark gray for headings */
        }
        h2 {
          font-size: 24px;
          font-weight: bold;
        }
        h3 {
          font-size: 18px;
          font-weight: 600;
        }
        p {
          font-size: 16px;
          color: #666666; /* Slightly lighter gray for body text */
          line-height: 1.5;
        }
        ul {
          font-size: 16px;
          color: #666666;
        }
        li {
          margin-bottom: 10px;
        }
        .highlight {
          font-weight: bold;
          color: #0066cc; /* Blue for highlights like dates or prices */
        }
        .footer {
          font-size: 14px;
          text-align: center;
          color: #999999; /* Light gray for footer text */
          margin-top: 20px;
        }
        .cta-link {
          font-weight: bold;
          color: #0066cc;
          text-decoration: none;
        }
      </style>
    </head>
    <body>

      <table>
        <tr>
          <td>
            <h2>Course Enrollment Confirmation</h2>
            <p>Dear <strong>{registrant_name},</strong></p>
            <p>We are pleased to inform you that your registration for the <strong>Introduction to Artificial Intelligence</strong> course has been successfully received.</p>

            <h3>Course Details:</h3>
            <p><strong>Duration:</strong> 4 weeks, with 8 hours of training per week.</p>
            <p><strong>Start Date:</strong> <span class="highlight">Thursday, February 19</span></p>
            <p><strong>Location:</strong> <a href="https://maps.app.goo.gl/9wSnR8WJaHSmFYeH7" class="cta-link" target="_blank">Federal Technical and Vocational Training Institute (FTVTI)</a> (In-person classes).</p>
            <p><strong>For Online Classes:</strong> You will be provided with the LMS link prior to the start date.</p>

            <h3>Payment Details:</h3>
            <ul>
              <li><strong>Original Course Fee:</strong> <span class="highlight">10,000 Birr</span></li>
              <li><strong>Promotional Discount:</strong> <span class="highlight">25%</span></li>
              <li><strong>Final Discounted Price:</strong> <span class="highlight">7,500 Birr</span></li>
              <li><strong>Bank:</strong> Bank of Abyssinia</li>
              <li><strong>Account Name:</strong> AFIRICAN DIGITAL AND INNOVATION TECHNOLOGY ACADEMY</li>
              <li><strong>Account Number:</strong> 229456048</li>
            </ul>
            <p>After making the payment, kindly send a payment screenshot to our Telegram account: <a href="https://t.me/adit_academy?direct" class="cta-link" target="_blank">@adit_academy</a></p>

            <div class="footer">
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
        if CustomCourseEnrollment.objects.filter(email=value).exists():
            raise serializers.ValidationError({
                "error": "EMAIL_EXISTS",
                "message": "An enrollment with this email already exists."
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
