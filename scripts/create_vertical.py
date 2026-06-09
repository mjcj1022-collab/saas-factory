#!/usr/bin/env python3
"""
SaaS Factory Vertical Generator
Usage: python scripts/create_vertical.py <vertical_name>
Example: python scripts/create_vertical.py insurance
"""
import os
import sys

MODELS_TEMPLATE = '''import uuid
from django.db import models


class {Name}Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="active")
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "{name}_records"
'''

URLS_TEMPLATE = '''from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
urlpatterns = [path("", include(router.urls))]
'''

APPS_TEMPLATE = '''from django.apps import AppConfig

class {Name}Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.{name}"
'''

INIT_TEMPLATE = ''


def create_vertical(name: str):
    app_dir = os.path.join("apps", name)
    if os.path.exists(app_dir):
        print(f"Vertical '{name}' already exists at {app_dir}")
        sys.exit(1)

    os.makedirs(app_dir)
    files = {
        "__init__.py": INIT_TEMPLATE,
        "models.py": MODELS_TEMPLATE.format(Name=name.capitalize(), name=name),
        "urls.py": URLS_TEMPLATE,
        "apps.py": APPS_TEMPLATE.format(Name=name.capitalize(), name=name),
        "tasks.py": f'from celery import shared_task\n\n# {name} tasks\n',
        "services.py": f'# {name} business logic\n',
        "serializers.py": f'from rest_framework import serializers\n# {name} serializers\n',
        "views.py": f'from rest_framework import viewsets\n# {name} viewsets\n',
        "admin.py": f'from django.contrib import admin\n# {name} admin\n',
    }

    for filename, content in files.items():
        filepath = os.path.join(app_dir, filename)
        with open(filepath, "w") as f:
            f.write(content)

    print(f"✓ Vertical '{name}' created at {app_dir}")
    print(f"\nNext steps:")
    print(f"  1. Add 'apps.{name}' to INSTALLED_APPS in config/settings.py")
    print(f"  2. Add URL route in config/urls.py:")
    print(f"     path('api/{name}/', include('apps.{name}.urls')),")
    print(f"  3. Define your models in apps/{name}/models.py")
    print(f"  4. Run: python manage.py makemigrations {name}")
    print(f"  5. Run: python manage.py migrate")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/create_vertical.py <name>")
        sys.exit(1)
    create_vertical(sys.argv[1].lower())
