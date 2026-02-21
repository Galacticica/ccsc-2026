"""Prompt helpers for conversation model interactions."""

from __future__ import annotations

from conversations.models import Conversation


def get_base_context(conversation: Conversation | None) -> str:
    """Return the base context for a conversation.

    The base context includes:
    1) selected AI model description
    2) descriptions for all quirks attached to that model
    """
    if not conversation or not conversation.model:
        return ""

    model_description = (conversation.model.description or "").strip()
    quirk_descriptions = [
        quirk.description.strip()
        for quirk in conversation.model.quirk.all()
        if quirk.description and quirk.description.strip()
    ]

    context_parts = []
    if model_description:
        context_parts.append(f"Model description:\n{model_description}")
    if quirk_descriptions:
        context_parts.append("Quirk descriptions:\n These are requirements for the AI model, even if it means slightly overriding the model description:\n" + "\n".join(f"- {text}" for text in quirk_descriptions))

    return "\n\n".join(context_parts)


def get_prompt(conversation: Conversation | None, user_message: str) -> str:
    """Build a prompt where system context comes from the selected model description."""
    base_context = get_base_context(conversation)
    user_message = (user_message or "").strip()

    if base_context:
        return f"System context to follow:\n{base_context}\n\nUser message to respond to:\n{user_message}"

    return f"User message:\n{user_message}"
