from django_filters import rest_framework as filters
from .models import Message

class MessageFilter(filters.FilterSet):
    """Filter class for Message model"""
    start_date = filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    sender = filters.UUIDFilter(field_name='sender_id__user_id')
    conversation = filters.UUIDFilter(field_name='conversation__conversation_id')

    class Meta:
        model = Message
        fields = ['start_date', 'end_date', 'sender', 'conversation'] 