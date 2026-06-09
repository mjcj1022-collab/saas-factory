from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.events"

    def ready(self):
        from core.events.consumers import register_all
        register_all()
