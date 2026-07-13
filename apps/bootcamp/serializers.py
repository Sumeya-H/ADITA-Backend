from datetime import date
from rest_framework import serializers
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from .models import BootcampRegistration


# ── Helper: calculate age from date of birth ──────────────────────────────────

def calculate_age(dob: date) -> int:
    today = date.today()
    return today.year - dob.year - (
        (today.month, today.day) < (dob.month, dob.day)
    )


# ── Serializer ────────────────────────────────────────────────────────────────

class BootcampRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = BootcampRegistration
        fields = "__all__"
        read_only_fields = [
            "id",
            "payment_status",
            "payment_confirmed_at",
            "payment_notes",
            "registered_at",
            "updated_at",
        ]
        extra_kwargs = {
            # receipt is a file upload — handle as multipart
            "payment_receipt": {"required": True},
        }

    # ── Field-level validation ────────────────────────────────────────────

    def validate_email(self, value):
        if BootcampRegistration.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "An application with this email address already exists."
            )
        return value

    def validate_phone(self, value):
        if BootcampRegistration.objects.filter(phone=value).exists():
            raise serializers.ValidationError(
                "An application with this phone number already exists."
            )
        return value

    def validate_agreed_terms(self, value):
        if not value:
            raise serializers.ValidationError(
                "You must agree to the terms of participation."
            )
        return value

    def validate_agreed_data_policy(self, value):
        if not value:
            raise serializers.ValidationError(
                "You must consent to ADITA's data privacy policy."
            )
        return value

    def validate_agreed_attendance_commitment(self, value):
        if not value:
            raise serializers.ValidationError(
                "You must commit to attending at least 8 of the 10 bootcamp days."
            )
        return value

    # ── Object-level validation ───────────────────────────────────────────

    def validate(self, data):
        dob = data.get("date_of_birth")
        applicant_type = data.get("applicant_type")

        if dob:
            age = calculate_age(dob)

            # Under-18 applicants must be high school students
            if age < 18 and applicant_type != "high_school_student":
                raise serializers.ValidationError({
                    "applicant_type": (
                        "Applicants under 18 must select 'High School Student' as their applicant type."
                    )
                })

            # Under-18: guardian fields required
            if age < 18:
                if not data.get("guardian_name", "").strip():
                    raise serializers.ValidationError({
                        "guardian_name": "Guardian name is required for applicants under 18."
                    })
                if not data.get("guardian_phone", "").strip():
                    raise serializers.ValidationError({
                        "guardian_phone": "Guardian phone number is required for applicants under 18."
                    })
                if not data.get("guardian_consent"):
                    raise serializers.ValidationError({
                        "guardian_consent": (
                            "Parent/guardian consent confirmation is required for applicants under 18."
                        )
                    })

        return data

    # ── Create: save then send confirmation email ─────────────────────────

    def create(self, validated_data):
        instance = super().create(validated_data)

        try:
            send_bootcamp_confirmation_email(
                full_name=instance.full_name,
                recipient_email=instance.email,
                registration_id=str(instance.id),
            )
        except Exception as e:
            # Never block registration if email fails
            print(f"[Bootcamp] Confirmation email failed for {instance.email}: {e}")

        return instance


# ── Email: application received ───────────────────────────────────────────────

def send_bootcamp_confirmation_email(full_name: str, recipient_email: str, registration_id: str):
    subject = "Your application is received — Build the Product · ADITA AI Sprint Bootcamp"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"><title>Application Received</title></head>
    <body style="margin:0; padding:0; font-family: Arial, sans-serif; background:#f4f4f4;">

      <table width="100%" cellpadding="0" cellspacing="0" style="padding:20px 0;">
        <tr>
          <td align="center">
            <table width="600" cellpadding="0" cellspacing="0"
                   style="background:#ffffff; border-radius:10px; overflow:hidden;">

              <!-- Header -->
              <tr>
                <td style="background:#52331E; padding:28px 30px; text-align:center;">
                  <p style="margin:0 0 4px 0; color:#F4A261; font-size:12px;
                             font-weight:bold; letter-spacing:2px; text-transform:uppercase;">
                    ADITA · AI Product Sprint Bootcamp
                  </p>
                  <h1 style="margin:0; color:#ffffff; font-size:22px; font-weight:bold;">
                    Build the Product
                  </h1>
                </td>
              </tr>

              <!-- Body -->
              <tr>
                <td style="padding:32px 30px; color:#333333;">

                  <h2 style="margin:0 0 16px 0; color:#52331E; font-size:18px;">
                    Hello {full_name}, your application is received! 🎉
                  </h2>

                  <p style="margin:0 0 16px 0; line-height:1.6;">
                    Thank you for applying to <strong>Build the Product — the ADITA AI Product Sprint Bootcamp</strong>.
                    We have received your application and payment receipt.
                  </p>

                  <p style="margin:0 0 16px 0; line-height:1.6;">
                    Our team will review your application and verify your payment. You will receive a
                    <strong>second email confirming your place</strong> once the review is complete.
                  </p>

                  <!-- Info box -->
                  <table width="100%" cellpadding="0" cellspacing="0"
                         style="background:#FDF6EE; border:1px solid #e8d5ab;
                                border-radius:8px; margin:24px 0;">
                    <tr>
                      <td style="padding:20px 24px;">
                        <p style="margin:0 0 12px 0; font-weight:bold; color:#52331E; font-size:14px;">
                          Bootcamp Details
                        </p>
                        <p style="margin:0 0 8px 0; font-size:14px; color:#555;">
                          📅 <strong>Start Date:</strong> August 10, 2025
                        </p>
                        <p style="margin:0 0 8px 0; font-size:14px; color:#555;">
                          📍 <strong>Location:</strong> Addis Ababa — Venue TBC
                        </p>
                        <p style="margin:0 0 8px 0; font-size:14px; color:#555;">
                          ⏱ <strong>Duration:</strong> 2 Weeks · 10 Days
                        </p>
                        <p style="margin:0; font-size:14px; color:#555;">
                          🎤 <strong>Online Orientation:</strong> Date will be announced on Telegram
                        </p>
                      </td>
                    </tr>
                  </table>

                  <!-- What's next -->
                  <p style="margin:0 0 12px 0; font-weight:bold; color:#52331E;">What happens next:</p>
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="padding:0 0 10px 0; font-size:14px; color:#555; line-height:1.6;">
                        ✅ &nbsp;ADITA reviews your application and payment receipt
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:0 0 10px 0; font-size:14px; color:#555; line-height:1.6;">
                        ✅ &nbsp;You receive a confirmation email with your venue and team details
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:0 0 10px 0; font-size:14px; color:#555; line-height:1.6;">
                        ✅ &nbsp;Join the Telegram channels below for updates and pre-bootcamp materials
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:0 0 10px 0; font-size:14px; color:#555; line-height:1.6;">
                        ✅ &nbsp;Attend the online orientation (date announced on Telegram)
                      </td>
                    </tr>
                  </table>

                  <!-- Telegram buttons -->
                  <p style="margin:24px 0 12px 0; font-weight:bold; color:#52331E;">Join our Telegram channels now:</p>
                  <table cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="padding-right:12px;">
                        <a href="https://t.me/aditacademy"
                           style="display:inline-block; background:#52331E; color:#ffffff;
                                  padding:12px 20px; text-decoration:none; border-radius:6px;
                                  font-weight:bold; font-size:14px;">
                          ADITA Channel
                        </a>
                      </td>
                      <td>
                        <a href="https://t.me/buildtheproduct"
                           style="display:inline-block; background:#F4A261; color:#52331E;
                                  padding:12px 20px; text-decoration:none; border-radius:6px;
                                  font-weight:bold; font-size:14px;">
                          Build the Product Group
                        </a>
                      </td>
                    </tr>
                  </table>

                  <p style="margin:28px 0 0 0; font-size:13px; color:#888; line-height:1.6;">
                    If you have any questions, reply to this email or contact us at
                    <a href="mailto:info@aditacademy.co" style="color:#52331E;">info@aditacademy.co</a>.
                  </p>

                  <p style="margin:20px 0 0 0; color:#52331E; font-size:14px;">
                    See you on August 10,<br>
                    <strong>The ADITA Team</strong>
                  </p>

                </td>
              </tr>

              <!-- Footer -->
              <tr>
                <td style="background:#FDF6EE; padding:16px 30px;
                           text-align:center; font-size:12px; color:#999;
                           border-top:1px solid #e8d5ab;">
                  © 2025 Africa Digital & Innovation Technology Academy (ADITA)<br>
                  IT Park, Addis Ababa, Ethiopia · info@aditacademy.co
                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>

    </body>
    </html>
    """

    text_content = f"""
Hello {full_name},

Your application for Build the Product — ADITA AI Product Sprint Bootcamp has been received.

Our team will review your application and payment receipt. You will receive a confirmation email once the review is complete.

BOOTCAMP DETAILS
Start Date: August 10, 2025
Location: Addis Ababa — Venue TBC
Duration: 2 Weeks · 10 Days
Online Orientation: Date will be announced on Telegram

WHAT HAPPENS NEXT
1. ADITA reviews your application and payment receipt
2. You receive a confirmation email with your venue and team details
3. Join the Telegram channels for updates and pre-bootcamp materials
4. Attend the online orientation (date announced on Telegram)

JOIN TELEGRAM
ADITA Channel: https://t.me/aditacademy
Build the Product Group: https://t.me/buildtheproduct

Questions? Email info@aditacademy.co

See you on August 10,
The ADITA Team

© 2025 Africa Digital & Innovation Technology Academy (ADITA)
IT Park, Addis Ababa, Ethiopia
    """

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)


# ── Payment-confirmed email (called manually from admin after review) ─────────

def send_bootcamp_payment_confirmed_email(full_name: str, recipient_email: str):
    subject = "Payment confirmed — You're in! Build the Product · ADITA Bootcamp"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"></head>
    <body style="margin:0; padding:0; font-family: Arial, sans-serif; background:#f4f4f4;">

      <table width="100%" cellpadding="0" cellspacing="0" style="padding:20px 0;">
        <tr>
          <td align="center">
            <table width="600" cellpadding="0" cellspacing="0"
                   style="background:#ffffff; border-radius:10px; overflow:hidden;">

              <tr>
                <td style="background:#52331E; padding:28px 30px; text-align:center;">
                  <p style="margin:0 0 4px 0; color:#F4A261; font-size:12px;
                             font-weight:bold; letter-spacing:2px; text-transform:uppercase;">
                    ADITA · AI Product Sprint Bootcamp
                  </p>
                  <h1 style="margin:0; color:#ffffff; font-size:22px;">Build the Product</h1>
                </td>
              </tr>

              <tr>
                <td style="padding:32px 30px; color:#333333;">
                  <h2 style="margin:0 0 16px 0; color:#52331E;">
                    Hello {full_name}, you're confirmed! 🚀
                  </h2>
                  <p style="margin:0 0 16px 0; line-height:1.6;">
                    Your payment has been verified and your place in
                    <strong>Build the Product</strong> is confirmed.
                  </p>
                  <p style="margin:0 0 16px 0; line-height:1.6;">
                    Your venue assignment and team details will be shared before the bootcamp starts.
                    Watch the Telegram channels for your pre-bootcamp materials and orientation date.
                  </p>
                  <p style="margin:0 0 8px 0; font-weight:bold; color:#52331E; font-size:14px;">
                    📅 Start Date: August 10, 2025
                  </p>
                  <p style="margin:0 0 24px 0; font-size:14px; color:#555;">
                    📍 Location: Addis Ababa — Venue TBC (check Telegram for updates)
                  </p>

                  <table cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="padding-right:12px;">
                        <a href="https://t.me/aditacademy"
                           style="display:inline-block; background:#52331E; color:#ffffff;
                                  padding:12px 20px; text-decoration:none; border-radius:6px;
                                  font-weight:bold; font-size:14px;">
                          ADITA Channel
                        </a>
                      </td>
                      <td>
                        <a href="https://t.me/buildtheproduct"
                           style="display:inline-block; background:#F4A261; color:#52331E;
                                  padding:12px 20px; text-decoration:none; border-radius:6px;
                                  font-weight:bold; font-size:14px;">
                          Build the Product Group
                        </a>
                      </td>
                    </tr>
                  </table>

                  <p style="margin:28px 0 0 0; color:#52331E; font-size:14px;">
                    We can't wait to build with you,<br>
                    <strong>The ADITA Team</strong>
                  </p>
                </td>
              </tr>

              <tr>
                <td style="background:#FDF6EE; padding:16px 30px;
                           text-align:center; font-size:12px; color:#999;
                           border-top:1px solid #e8d5ab;">
                  © 2025 Africa Digital & Innovation Technology Academy (ADITA)<br>
                  IT Park, Addis Ababa, Ethiopia
                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>

    </body>
    </html>
    """

    text_content = f"""
Hello {full_name},

Your payment has been verified and your place in Build the Product is confirmed!

Start Date: August 10, 2025
Location: Addis Ababa — Venue TBC

Watch the Telegram channels for your orientation date and pre-bootcamp materials.

ADITA Channel: https://t.me/aditacademy
Build the Product Group: https://t.me/buildtheproduct

We can't wait to build with you,
The ADITA Team
    """

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
