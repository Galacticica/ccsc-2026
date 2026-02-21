from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Conversation, Message


class MessageInline(TabularInline):
    model = Message
    extra = 1


@admin.register(Conversation)
class ConversationAdmin(ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ('sender', 'conversation', 'timestamp')

