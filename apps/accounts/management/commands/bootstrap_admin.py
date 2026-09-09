"""Create the first administrator from operator-supplied environment variables."""
import os

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email
from django.db import connection, transaction


class Command(BaseCommand):
    help = "Create the first admin once; never promote users or reset passwords."

    def handle(self, *args, **options):
        email = os.environ.get("ZAOUIA_ADMIN_EMAIL", "").strip()
        password = os.environ.get("ZAOUIA_ADMIN_PASSWORD", "")
        if not email and not password:
            self.stdout.write("Admin bootstrap skipped: no credentials configured.")
            return
        if not email or not password:
            raise CommandError("Set both ZAOUIA_ADMIN_EMAIL and ZAOUIA_ADMIN_PASSWORD.")

        User = get_user_model()
        email = User.objects.normalize_email(email)
        try:
            validate_email(email)
        except ValidationError:
            raise CommandError("Admin email is invalid.") from None

        with transaction.atomic():
            # Serialize first-admin creation across overlapping PostgreSQL deploys.
            if connection.vendor == "postgresql":
                with connection.cursor() as cursor:
                    cursor.execute("SELECT pg_advisory_xact_lock(%s)", [90420901])
            existing = User.objects.filter(email__iexact=email).first()
            if existing:
                if existing.is_superuser and existing.is_staff and existing.is_active:
                    self.stdout.write("Admin already exists; credentials unchanged.")
                    return
                raise CommandError("Email belongs to an existing account; no changes made.")
            if User.objects.filter(is_superuser=True).exists():
                raise CommandError("An administrator already exists; bootstrap refused.")
            candidate = User(email=email)
            try:
                validate_password(password, user=candidate)
                if len(password) < 12:
                    raise ValidationError("Minimum bootstrap password length is 12.")
            except ValidationError:
                raise CommandError(
                    "Choose a password of at least 12 characters that passes password validation."
                ) from None
            User.objects.create_superuser(email=email, password=password)
        self.stdout.write(self.style.SUCCESS("Initial administrator created."))
