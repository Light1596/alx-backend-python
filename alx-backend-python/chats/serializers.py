#!/usr/bin/env python3
"""
This module defines Django REST Framework serializers for the
User, Conversation, and Message models.
"""
from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.
    Includes only necessary fields for displaying user information.
    """
    class Meta:
        """Meta class for UserSerializer."""
        model = User
        fields = ['id', 'username', 'email'] # Only expose necessary user fields
        read_only_fields = ['username', 'email'] # Username and email are typically set once


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    Includes the sender's username for better readability in conversation views.
    """
    sender = UserSerializer(read_only=True) # Nested serializer for sender

    class Meta:
        """Meta class for MessageSerializer."""
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'timestamp']
        read_only_fields = ['id', 'timestamp'] # ID and timestamp are generated automatically


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.
    Includes nested messages and participant details.
    """
    # Use a custom field for participants to handle their display
    participants = UserSerializer(many=True, read_only=True)
    # Nested messages, ordered by timestamp
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        """Meta class for ConversationSerializer."""
        model = Conversation
        fields = ['id', 'subject', 'participants', 'messages', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        """
        Custom create method for ConversationSerializer to handle
        adding participants correctly.
        """
        # When creating a conversation, participants need to be passed separately
        # in the initial data (e.g., as a list of user IDs)
        # For simplicity, we'll assume participants are added after creation
        # or handle them in the view if creating from scratch.
        # This serializer is mainly for *reading* the conversation.

        # If you need to create a conversation with participants directly
        # from the serializer, you'd need to extract them from validated_data
        # and then add them after the Conversation instance is created.
        # For this setup, we'll assume participants are added in the view.
        return super().create(validated_data)