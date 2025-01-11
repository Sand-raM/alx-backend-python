from django.apps import AppConfig

class DjangoChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DjangoChat'

    def ready(self):
        from . import signals  # Make sure the signals are imported
