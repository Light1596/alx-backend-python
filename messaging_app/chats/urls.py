#!/usr/bin/env python3
"""
URL routing for the chats application.
Uses Django REST Framework's DefaultRouter for automatic URL generation.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ConversationViewSet, MessageViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]