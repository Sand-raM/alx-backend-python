from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User

# Signal for creating notifications
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

# Signal for logging message edits
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.id:  # Check if the instance already exists
        previous_message = Message.objects.get(id=instance.id)
        if previous_message.content != instance.content:
            instance.edited = True
            MessageHistory.objects.create(
                original_message=previous_message,
                content=previous_message.content,
                edited_by=instance.sender
            )

# Signal for deleting user-related data
@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()
