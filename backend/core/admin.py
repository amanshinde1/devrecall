from django.contrib import admin
from .models import Topic, Pattern, Problem, RecallLog


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(Pattern)
class PatternAdmin(admin.ModelAdmin):
    list_display = ("name", "topic", "created_at")
    list_filter = ("topic",)
    search_fields = ("name",)


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("title", "pattern", "difficulty", "created_at")
    list_filter = ("difficulty", "pattern")
    search_fields = ("title",)


@admin.register(RecallLog)
class RecallLogAdmin(admin.ModelAdmin):
    list_display = ("user","problem", "solved", "confidence", "created_at")
    list_filter = ("solved", "confidence")
