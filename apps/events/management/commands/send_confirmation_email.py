from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from apps.events.models import CustomCourseEnrollment
from apps.events.serializers import send_course_confirmation_email


class Command(BaseCommand):
    help = 'Send enrollment confirmation emails to all registered users'

    def handle(self, *args, **kwargs):
        users = CustomCourseEnrollment.objects.all()

        for user in users:
            registrant_name = f"{user.first_name} {user.last_name}"
            self.stdout.write(
                f"Sending email to {registrant_name} ({user.email})...")
            send_course_confirmation_email(None, registrant_name, user.email)
            self.stdout.write(self.style.SUCCESS(
                f"Successfully sent email to {registrant_name}"))
        # self.stdout.write(
        #    f"Sending email to Kalab Kassa kalabkassa@gmail.com ...")
        # Calls your existing email function
        # send_course_confirmation_email(
        #    None, "Kalab Kassa", "kalabkassa@gmail.com")
        # self.stdout.write(self.style.SUCCESS(
        #    f"Successfully sent email to kalab kassa"))
