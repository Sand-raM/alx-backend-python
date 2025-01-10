from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from .filters import MessageFilter
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsOwner, IsAuthenticatedAndParticipant,IsParticipantOfConversation
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsOwner, IsAuthenticatedAndParticipant, IsParticipantOfConversation]

    def get_queryset(self):
        # Filter conversations to only include the user's
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsOwner, IsAuthenticatedAndParticipant, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ['created_at']
    ordering = ['-created_at']  # Default ordering: newest first

    def get_queryset(self):
        # Filter messages to only include those in the user's conversations
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Send a new message to an existing conversation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

