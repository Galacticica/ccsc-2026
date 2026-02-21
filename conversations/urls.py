"""
File: urls.py
Author: Reagan Zierke
Date: 2026-02-21
Description: URL routes for conversation views.
"""

from django.urls import path

from . import views

urlpatterns = [
    path('chat', views.MainPageView.as_view(), name='main_page'),
    path('messages/send/', views.send_message, name='send_message'),
]
