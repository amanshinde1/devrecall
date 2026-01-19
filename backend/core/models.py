from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta


class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Pattern(models.Model):
    name = models.CharField(max_length=100)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="patterns"
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("name", "topic")

    def __str__(self):
        return f"{self.name} ({self.topic.name})"


class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    title = models.CharField(max_length=200)
    pattern = models.ForeignKey(
        Pattern,
        on_delete=models.CASCADE,
        related_name="problems"
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES
    )
    external_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class RecallLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recall_logs"
    )
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="recall_logs"
    )
    solved = models.BooleanField(default=False)
    confidence = models.PositiveSmallIntegerField()
    notes = models.TextField(blank=True, null=True)

    # 🔥 PHASE 3 — SPACED REPETITION FIELDS
    next_review_at = models.DateTimeField(null=True, blank=True)
    priority_score = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_review_schedule(self):
        """
        Simple, explainable spaced repetition logic.
        """

        confidence_intervals = {
            1: 1,
            2: 1,
            3: 3,
            4: 7,
            5: 14,
        }

        days = confidence_intervals.get(self.confidence, 3)

        # Unsolved problems need faster review
        if not self.solved:
            days = max(1, days // 2)

        self.next_review_at = timezone.now() + timedelta(days=days)

        # Higher = more urgent
        self.priority_score = (5 - self.confidence) + (2 if not self.solved else 0)

    def save(self, *args, **kwargs):
        self.calculate_review_schedule()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.problem.title}"
