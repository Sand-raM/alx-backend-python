from django_filters import rest_framework as filters
from .models import Message

class MessageFilter(filters.FilterSet):
    sender = filters.CharFilter(field_name="sender__username", lookup_expr="icontains")
    recipient = filters.CharFilter(field_name="recipient__username", lookup_expr="icontains")
    created_at = filters.DateFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'created_at']
