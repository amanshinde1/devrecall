from rest_framework import serializers
from .models import Topic, Pattern, Problem, RecallLog


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["id", "name", "created_at"]
        read_only_fields = ["id", "created_at"]


class PatternSerializer(serializers.ModelSerializer):
    topic = serializers.StringRelatedField()

    class Meta:
        model = Pattern
        fields = ["id", "name", "topic", "description", "created_at"]
        read_only_fields = ["id", "created_at"]


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
        read_only_fields = ["id", "created_at"]


class RecallLogSerializer(serializers.ModelSerializer):
    # user is always controlled by backend
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

    # ---------- FIELD LEVEL VALIDATION ----------
    def validate_confidence(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError(
                "Confidence must be between 1 and 5."
            )
        return value

    # ---------- OBJECT LEVEL VALIDATION ----------
    def validate(self, data):
        solved = data.get("solved")
        confidence = data.get("confidence")
        notes = data.get("notes")

        # If marked solved, confidence should not be very low
        if solved and confidence is not None and confidence < 3:
            raise serializers.ValidationError(
                "Solved problems should have confidence 3 or higher."
            )

        # Low confidence requires reflection
        if confidence is not None and confidence <= 3 and not notes:
            raise serializers.ValidationError(
                "Please add notes when confidence is 3 or lower."
            )

        return data
