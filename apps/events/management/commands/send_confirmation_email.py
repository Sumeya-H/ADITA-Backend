from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from apps.events.models import CustomCourseEnrollment, EventRegistration
from apps.events.serializers import send_course_confirmation_email, send_in_person_email, send_virtual_email, send_virtual_not_confirmed_email

LIMIT = 150
OFFSET = 0 # 👈 change this each time you rerun

class Command(BaseCommand):
    help = 'Send enrollment confirmation emails to all registered users'

    def handle(self, *args, **kwargs):
        users = EventRegistration.objects.all().order_by("registered_at")[OFFSET:OFFSET + LIMIT]

        self.stdout.write(f"Sending users from {OFFSET} to {OFFSET + LIMIT}")

        for index, user in enumerate(users, start=OFFSET):
            try:
                registrant_name = user.full_name

                self.stdout.write(
                    f"[{index}] Sending to {registrant_name} ({user.email})"
                )

                if user.attendance_type == "in_person":
                    send_in_person_email(None, registrant_name, user.email)

                elif user.attendance_type == "virtual":
                    send_virtual_email(None, registrant_name, user.email)

                else:
                    send_virtual_not_confirmed_email(None, registrant_name, user.email)

                self.stdout.write(
                    self.style.SUCCESS(f"[{index}] Sent successfully")
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"[{index}] Failed: {user.email} → {str(e)}")
                )

        self.stdout.write(self.style.SUCCESS("Batch complete."))

        # self.stdout.write(
        #    f"Sending email to Kalab Kassa kalabkassa@gmail.com ...")
        # send_course_confirmation_email(
        #    None, "Dr. Sultan Feisso", "sultanmeko2@gmail.com", "1389076f-2696-43cd-8b63-e98342b78275")
        # self.stdout.write(self.style.SUCCESS(
        #    f"Successfully sent email to kalab kassa"))
