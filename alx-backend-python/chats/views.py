#!/usr/bin/env python3
"""
This module defines Django REST Framework ViewSets for handling
Conversation and Message API endpoints.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q # For complex lookups
from .models import User, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing and listing users.
    Only allows read operations for security.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing conversation instances.
    Provides endpoints for listing, retrieving, creating, updating, and deleting conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned conversations to those
        the current user is a participant of.
        For simplicity, it returns all for now, but in a real app,
        you'd filter by request.user.
        """
        # Example for filtering by current user (requires authentication setup)
        # if self.request.user.is_authenticated:
        #     return Conversation.objects.filter(participants=self.request.user).distinct()
        return super().get_queryset()

    # REMOVE 'help_text' FROM HERE
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """
        Send a new message within this conversation.
        Expected request body: {"content": "Your message content"}
        The sender is assumed to be the authenticated user.
        """
        conversation = self.get_object()
        user = request.user # Assumes user is authenticated

        if not user.is_authenticated:
            return Response({"detail": "Authentication required to send messages."},
                            status=status.HTTP_401_UNAUTHORIZED)

        # Check if the user is a participant in the conversation
        if user not in conversation.participants.all():
            return Response({"detail": "You are not a participant in this conversation."},
                            status=status.HTTP_403_FORBIDDEN)

        content = request.data.get('content')
        if not content:
            return Response({"content": "This field is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            conversation=conversation,
            sender=user,
            content=content
        )
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # REMOVE 'help_text' FROM HERE
    @action(detail=False, methods=['post'])
    def create_conversation(self, request):
        """
        Create a new conversation with specified participants.
        Expected request body: {
            "subject": "Optional conversation subject",
            "participant_ids": [1, 2, 3]
        }
        The requesting user will automatically be added as a participant.
        """
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "Authentication required to create conversations."},
                            status=status.HTTP_401_UNAUTHORIZED)

        subject = request.data.get('subject')
        participant_ids = request.data.get('participant_ids', [])

        # Ensure the requesting user is always a participant
        if user.id not in participant_ids:
            participant_ids.append(user.id)

        # Validate participant IDs exist
        participants = User.objects.filter(id__in=participant_ids)
        if len(participants) != len(participant_ids):
            return Response({"participant_ids": "One or more participant IDs are invalid."},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create(subject=subject)
        conversation.participants.set(participants) # Use set() to add many-to-many relationships
        conversation.save()

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing messages.
    Messages are typically created via the ConversationViewSet's send_message action.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned messages to those
        within conversations the current user is a participant of.
        """
        # Example for filtering by current user
        # if self.request.user.is_authenticated:
        #     user_conversations = self.request.user.conversations.all()
        #     return Message.objects.filter(conversation__in=user_conversations).distinct()
        return super().get_queryset()