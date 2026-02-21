"""
File: urls.py
Author: Reagan Zierke
Date: 2026-02-21
Description: description
"""

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
]