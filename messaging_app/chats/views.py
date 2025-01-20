from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer, 
    ConversationCreateSerializer,
    MessageSerializer,
    MessageCreateSerializer
)
from .permissions import IsParticipantOfConversation, IsOwnerOrReadOnly
from .filters import MessageFilter

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing conversations.
    """
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    queryset = Conversation.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['created_at']
    search_fields = ['participants_id__email', 'participants_id__first_name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer
    
    def get_queryset(self):
        """Filter conversations to only those the user participates in."""
        return self.queryset.filter(participants_id=self.request.user)
    
    def perform_create(self, serializer):
        """Create a new conversation and add initial message if provided."""
        conversation = serializer.save()
        conversation.participants_id.add(self.request.user)
        
        initial_message = serializer.validated_data.get('initial_message')
        if initial_message:
            Message.objects.create(
                sender_id=self.request.user,
                conversation=conversation,
                message_body=initial_message
            )
    
    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        """Add a participant to an existing conversation."""
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        conversation.participants_id.add(user_id)
        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_200_OK
        )

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and sending messages.
    """
    permission_classes = [IsAuthenticated, IsParticipantOfConversation, IsOwnerOrReadOnly]
    queryset = Message.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ['message_body', 'sender_id__email']
    ordering_fields = ['sent_at']
    ordering = ['sent_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer
    
    def get_queryset(self):
        """Filter messages to only those in conversations the user participates in."""
        queryset = self.queryset.filter(
            conversation__participants_id=self.request.user
        )
        return queryset.order_by('sent_at')
    
    def perform_create(self, serializer):
        """Create a new message."""
        conversation = get_object_or_404(
            Conversation, 
            conversation_id=serializer.validated_data['conversation'].conversation_id,
            participants_id=self.request.user
        )
        
        serializer.save(
            sender_id=self.request.user,
            conversation=conversation
        )