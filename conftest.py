import django
from django.conf import settings


def pytest_configure(config):
    """Override settings before tests run."""
    # Patch Celery to use in-memory broker during tests
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True
    settings.CELERY_BROKER_URL = "memory://"
    settings.CELERY_RESULT_BACKEND = "cache+memory://"
