from rest_framework import serializers
from .models import User, Message, Conversation

# Serializer for the User model.
# This serializer handles the serialization and deserialization of the User model.
# It ensures data related to users (e.g., creating a new user, updating a user) is validated and formatted properly.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'firstname', 'last_name', 'email','phone_number', 'role', 'created_at' ]

# Serializer for the Message model.
# This serializer is responsible for validating and formatting message data.
# It supports the relationship between a message and its sender or conversation.
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

# Serializer for the Conversation model.
# This serializer includes nested data, linking participants and messages within a conversation.
# It is crucial for retrieving conversation details with all associated messages.
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, ready_only=True) # Many-to-many relationship
    messages = MessageSerializer(many=True, read_only=True) # One-to-many relationship

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']