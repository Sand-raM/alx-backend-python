from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    # Check if the message is being edited
    if instance.pk:  # Check if the message exists (i.e., it's being updated)
        old_message = Message.objects.get(pk=instance.pk)
        
        if old_message.content != instance.content:  # If the content is different, it's being edited
            # Log the old message content into the MessageHistory model
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content
            )
            instance.edited = True  # Mark the message as edited
