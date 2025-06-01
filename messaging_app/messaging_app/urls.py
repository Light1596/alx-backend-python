#!/usr/bin/env python3
"""
messaging_app URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')), # Include chats app URLs under /api/
]