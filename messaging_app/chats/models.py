#!/usr/bin/env python3
"""
This module defines the data models for the messaging application,
including User, Conversation, and Message models.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    This model can be extended with additional fields specific to the messaging app.
    For this project, we primarily rely on the fields provided by AbstractUser.
    """
    # Example: You could add a profile picture or status here if needed
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    # status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        """Meta class for User model."""
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['username']

    def __str__(self) -> str:
        """String representation of the User model."""
        return self.username


class Conversation(models.Model):
    """
    Represents a conversation between multiple users.
    A conversation has a subject and can involve multiple users.
    """
    subject = models.CharField(max_length=255, blank=True, null=True,
                               help_text="Optional subject for the conversation")
    # Many-to-many relationship with User through a through table
    participants = models.ManyToManyField(
        User,
        related_name='conversations',
        help_text="Users involved in this conversation"
    )
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text="Timestamp when the conversation was created")
    updated_at = models.DateTimeField(auto_now=True,
                                      help_text="Timestamp when the conversation was last updated")

    class Meta:
        """Meta class for Conversation model."""
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        ordering = ['-updated_at'] # Order by most recently updated conversation

    def __str__(self) -> str:
        """String representation of the Conversation model."""
        participant_names = ", ".join([p.username for p in self.participants.all()])
        return f"Conversation with: {participant_names} (Subject: {self.subject or 'No Subject'})"


class Message(models.Model):
    """
    Represents a single message within a conversation.
    Each message belongs to a sender and a conversation.
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text="The conversation this message belongs to"
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text="The user who sent this message"
    )
    content = models.TextField(help_text="The content of the message")
    timestamp = models.DateTimeField(auto_now_add=True,
                                     help_text="Timestamp when the message was sent")

    class Meta:
        """Meta class for Message model."""
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['timestamp'] # Order messages chronologically

    def __str__(self) -> str:
        """String representation of the Message model."""
        return f"Message from {self.sender.username} in {self.conversation.id}: {self.content[:50]}..."