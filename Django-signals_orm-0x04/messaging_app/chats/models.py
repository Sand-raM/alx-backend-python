from django.db import models

class Message(models.Model):
    sender = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # New field to track read status

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"

    # Create a custom manager for unread messages
    class UnreadMessagesManager(models.Manager):
        def unread_for_user(self, user):
            return self.filter(receiver=user, read=False).only('sender', 'content', 'timestamp')  # Optimize query with `.only()`

    # Add the custom manager to the model
    objects = models.Manager()  # Default manager
    unread_messages = UnreadMessagesManager()  # Custom manager
