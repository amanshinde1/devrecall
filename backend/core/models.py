from django.conf import settings
from django.db import models


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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.problem.title} - {self.created_at.date()}"
