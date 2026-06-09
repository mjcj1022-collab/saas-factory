# Celery app is imported explicitly by workers via: celery -A config worker
# Do NOT import it here — it causes circular import during Django startup.
