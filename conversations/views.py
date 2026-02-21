"""
File: views.py
Author: Reagan Zierke
Date: 2026-02-21
Description: description
"""

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View


class MainPageView(View):
    def get(self, request):
        return render(request, 'conversations/main_page.html')