from django.db import models
from django.contrib.auth.models import User

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        # Filters unread messages for a specific user
        return self.filter(receiver=user, read=False).only('sender', 'content', 'timestamp')

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    read = models.BooleanField(default=False)  # Added field to track if message is read
    
    objects = models.Manager()  # Default manager
    unread_messages = UnreadMessagesManager()  # Custom manager

    def __str__(self):
        return f'{self.sender} to {self.receiver} at {self.timestamp}'
    
    def get_replies(self):
        # Recursive query to fetch all replies for this message
        return Message.objects.filter(parent_message=self).order_by('timestamp')

    class Meta:
        ordering = ['timestamp']
