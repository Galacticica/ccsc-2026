"""
File: views.py
Author: Reagan Zierke
Date: 2026-02-21
Description: Main conversation page and chat message handling.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View

from ai_models.models import AIModel
from .models import Conversation, Message


class MainPageView(LoginRequiredMixin, View):
    def get(self, request):
        conversation = self._get_requested_conversation(request)
        messages = conversation.messages.order_by("timestamp") if conversation else []
        ai_models = AIModel.objects.order_by("name")
        selected_model = conversation.model if conversation else ai_models.order_by("?").first()
        model_locked = conversation.messages.exists() if conversation else False

        return render(
            request,
            "conversations/main_page.html",
            {
                "conversation": conversation,
                "messages": messages,
                "ai_models": ai_models,
                "selected_model": selected_model,
                "model_locked": model_locked,
            },
        )

    def _get_requested_conversation(self, request):
        conversation_id = request.GET.get("conversation_id")
        if not conversation_id:
            return None

        return get_object_or_404(Conversation, id=conversation_id, user=request.user)


@login_required
def send_message(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    content = request.POST.get("content", "").strip()
    if not content:
        return HttpResponseBadRequest("Message cannot be empty")

    conversation_id = request.POST.get("conversation_id")
    model_id = request.POST.get("model_id")

    if conversation_id:
        conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    else:
        selected_model = None
        if model_id:
            selected_model = get_object_or_404(AIModel, id=model_id)
        else:
            selected_model = AIModel.objects.order_by("?").first()

        conversation = Conversation.objects.create(user=request.user, model=selected_model)

    Message.objects.create(conversation=conversation, sender="user", content=content)

    messages = conversation.messages.order_by("timestamp")
    response = render(
        request,
        "conversations/partials/chat_shell.html",
        {
            "conversation": conversation,
            "messages": messages,
            "ai_models": AIModel.objects.order_by("name"),
            "selected_model": conversation.model,
            "model_locked": True,
        },
    )
    response["HX-Push-Url"] = f"{reverse('main_page')}?conversation_id={conversation.id}"
    return response
