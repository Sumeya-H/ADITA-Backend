from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from apps.events.models import CustomCourseEnrollment, EventRegistration
from apps.events.serializers import send_course_confirmation_email


class Command(BaseCommand):
    help = 'Send enrollment confirmation emails to all registered users'

    def handle(self, *args, **kwargs):
        users = EventRegistration.objects.all()

        for user in users:
            registrant_name = user.full_name
            if user.email == "kalabkassa@gmail.com":
                self.stdout.write(
                    f"Sending email to {registrant_name} ({user.email})...")
                send_course_confirmation_email(
                    None, registrant_name, user.email, user.id)
                self.stdout.write(self.style.SUCCESS(
                    f"Successfully sent email to {registrant_name}"))
        # self.stdout.write(
        #    f"Sending email to Kalab Kassa kalabkassa@gmail.com ...")
        # send_course_confirmation_email(
        #    None, "Dr. Sultan Feisso", "sultanmeko2@gmail.com", "1389076f-2696-43cd-8b63-e98342b78275")
        # self.stdout.write(self.style.SUCCESS(
        #    f"Successfully sent email to kalab kassa"))
