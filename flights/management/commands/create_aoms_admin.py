import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or update the AOMS production admin user"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.environ.get("AOMS_ADMIN_USERNAME")
        password = os.environ.get("AOMS_ADMIN_PASSWORD")
        email = os.environ.get("AOMS_ADMIN_EMAIL", "")

        if not username or not password:
            self.stdout.write(
                self.style.ERROR(
                    "AOMS_ADMIN_USERNAME and AOMS_ADMIN_PASSWORD "
                    "environment variables are required."
                )
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"AOMS admin user '{username}' created successfully."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"AOMS admin user '{username}' updated successfully."
                )
            )
