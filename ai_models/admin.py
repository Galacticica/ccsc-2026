from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import AIModel, AIQuirk


class AIQuirkInline(TabularInline):
    model = AIModel.quirk.through
    extra = 1


@admin.register(AIModel)
class AIModelAdmin(ModelAdmin):
    list_display = ('name', 'description')
    inlines = [AIQuirkInline]


@admin.register(AIQuirk)
class AIQuirkAdmin(ModelAdmin):
    list_display = ('name', 'description')
