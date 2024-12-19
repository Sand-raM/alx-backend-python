from rest_framework import serializers
from .models import User, Message, Conversation

# Serializer for the User model.
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)  # Custom field example

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at', 'full_name']

# Serializer for the Message model.
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

# Serializer for the Conversation model.
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)  # Many-to-many relationship
    messages = MessageSerializer(many=True, read_only=True)  # One-to-many relationship
    message_count = serializers.SerializerMethodField()  # Custom field for message count

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'message_count', 'created_at']

    def get_message_count(self, obj):
        # Custom logic to count the number of messages in a conversation
        return obj.messages.count()

    def validate(self, data):
        # Custom validation example
        if not data.get('participants'):
            raise serializers.ValidationError("A conversation must have at least one participant.")
        return data
