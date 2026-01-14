from rest_framework import serializers
from .models import Topic, Pattern, Problem, RecallLog


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["id", "name", "created_at"]


class PatternSerializer(serializers.ModelSerializer):
    topic = serializers.StringRelatedField()

    class Meta:
        model = Pattern
        fields = ["id", "name", "topic", "description", "created_at"]


class ProblemSerializer(serializers.ModelSerializer):
    pattern = serializers.StringRelatedField()

    class Meta:
        model = Problem
        fields = [
            "id",
            "title",
            "pattern",
            "difficulty",
            "external_link",
            "created_at",
        ]


class RecallLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = RecallLog
        fields = [
            "id",
            "user",
            "problem",
            "solved",
            "confidence",
            "notes",
            "created_at",
        ]
        read_only_fields = ["id", "user", "created_at"]
