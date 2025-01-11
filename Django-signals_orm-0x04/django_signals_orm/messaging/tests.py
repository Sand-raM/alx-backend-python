from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessagingTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender')
        self.receiver = User.objects.create_user(username='receiver')

    def test_message_creation_creates_notification(self):
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello")
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
