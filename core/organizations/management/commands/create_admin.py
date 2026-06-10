"""
Management command to create superuser non-interactively from env vars.
Usage: python manage.py create_admin
Env vars: ADMIN_EMAIL, ADMIN_PASSWORD (defaults provided for safety)
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create superuser from environment variables (non-interactive)"

    def handle(self, *args, **options):
        User = get_user_model()
        email = os.environ.get("ADMIN_EMAIL", "admin@saas-factory.app")
        password = os.environ.get("ADMIN_PASSWORD")

        if not password:
            self.stderr.write("Set ADMIN_PASSWORD env var before running this command.")
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(f"Admin user {email} already exists — skipping.")
            return

        from core.organizations.models import Organization
        import django.utils.text as slugify_module

        slug = "default-org"
        org, _ = Organization.objects.get_or_create(
            slug=slug,
            defaults={"name": "Default Organization", "plan": "enterprise"},
        )

        user = User.objects.create_superuser(
            username=email,
            email=email,
            password=password,
            first_name="Admin",
            last_name="User",
            organization=org,
            role="owner",
        )
        self.stdout.write(self.style.SUCCESS(f"Superuser created: {email}"))
