from django.db import models

class UnreadMessagesManager(models.Manager):
    def get_queryset(self):
        # Filters messages that are unread
        return super().get_queryset().filter(read=False)

    def for_user(self, user):
        # Filters unread messages for a specific user
        return self.get_queryset().filter(receiver=user)
