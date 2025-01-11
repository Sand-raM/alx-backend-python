from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
from .signals import create_notification

class MessagingConfig(AppConfig):
    name = 'messaging'

    def ready(self):
        import messaging.signals  # Ensure signals are registered on app startup
