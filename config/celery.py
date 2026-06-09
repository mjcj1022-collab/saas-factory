from __future__ import absolute_import, unicode_literals
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from celery import Celery  # noqa: E402

app = Celery("saas_factory")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
