from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.db.models import Count, Avg, Q

from .models import Topic, Pattern, Problem, RecallLog
from .serializers import (
    TopicSerializer,
    PatternSerializer,
    ProblemSerializer,
    RecallLogSerializer,
)


# --------------------
# READ APIs
# --------------------

class TopicListAPIView(ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class PatternListAPIView(ListAPIView):
    serializer_class = PatternSerializer

    def get_queryset(self):
        queryset = Pattern.objects.select_related("topic")
        topic_id = self.request.query_params.get("topic")
        if topic_id:
            queryset = queryset.filter(topic_id=topic_id)
        return queryset.order_by("name")


class ProblemListAPIView(ListAPIView):
    queryset = Problem.objects.select_related("pattern")
    serializer_class = ProblemSerializer


# --------------------
# RECALL LOG CRUD APIs
# --------------------

class RecallLogListCreateAPIView(ListAPIView, CreateAPIView):
    serializer_class = RecallLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecallLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecallLogUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = RecallLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecallLog.objects.filter(user=self.request.user)


class RecallLogDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecallLog.objects.filter(user=self.request.user)


# --------------------
# RECALL INTELLIGENCE APIs
# --------------------

class RecallSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = RecallLog.objects.filter(user=request.user)

        total_attempts = logs.count()
        solved_count = logs.filter(solved=True).count()
        accuracy = round((solved_count / total_attempts) * 100, 2) if total_attempts else 0

        return Response({
            "total_attempts": total_attempts,
            "solved": solved_count,
            "accuracy": accuracy,
        })


class RecallWeakPatternsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = (
            RecallLog.objects
            .filter(user=request.user)
            .values("problem__pattern__name")
            .annotate(
                attempts=Count("id"),
                solved=Count("id", filter=Q(solved=True)),
                avg_confidence=Avg("confidence"),
            )
        )

        response = []
        for item in logs:
            attempts = item["attempts"]
            solved = item["solved"]
            accuracy = round((solved / attempts) * 100, 2) if attempts else 0

            response.append({
                "pattern": item["problem__pattern__name"],
                "attempts": attempts,
                "solved": solved,
                "accuracy": accuracy,
                "avg_confidence": round(item["avg_confidence"], 2) if item["avg_confidence"] else 0,
            })

        response.sort(key=lambda x: x["accuracy"])
        return Response(response)


class RecallWeakProblemsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = (
            RecallLog.objects
            .filter(user=request.user)
            .values("problem__id", "problem__title", "problem__pattern__name")
            .annotate(
                attempts=Count("id"),
                solved=Count("id", filter=Q(solved=True)),
                avg_confidence=Avg("confidence"),
            )
        )

        weak_problems = []

        for item in logs:
            attempts = item["attempts"]
            solved = item["solved"]
            accuracy = round((solved / attempts) * 100, 2) if attempts else 0
            avg_conf = round(item["avg_confidence"], 2) if item["avg_confidence"] else 0

            if accuracy < 70 or avg_conf <= 3:
                weak_problems.append({
                    "problem_id": item["problem__id"],
                    "problem": item["problem__title"],
                    "pattern": item["problem__pattern__name"],
                    "attempts": attempts,
                    "solved": solved,
                    "accuracy": accuracy,
                    "avg_confidence": avg_conf,
                })

        weak_problems.sort(key=lambda x: (x["accuracy"], x["avg_confidence"]))
        return Response(weak_problems)


class RecallReviewQueueAPIView(APIView):
    """
    GET /api/recall-logs/analytics/review-queue/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = (
            RecallLog.objects
            .filter(user=request.user)
            .select_related("problem", "problem__pattern")
            .order_by("solved", "confidence", "-created_at")
        )

        seen = set()
        queue = []

        for log in logs:
            if log.problem_id in seen:
                continue
            seen.add(log.problem_id)

            queue.append({
                "problem_id": log.problem.id,
                "problem": log.problem.title,
                "pattern": log.problem.pattern.name,
                "last_solved": log.solved,
                "confidence": log.confidence,
                "last_attempt": log.created_at,
            })

        return Response(queue)


class RecallDailyPlanAPIView(APIView):
    """
    GET /api/recall-logs/analytics/daily-plan/?limit=5
    SQLite-safe spaced repetition scoring
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        limit = int(request.query_params.get("limit", 5))

        logs = (
            RecallLog.objects
            .filter(user=request.user)
            .select_related("problem", "problem__pattern")
            .order_by("-created_at")
        )

        # Keep latest attempt per problem
        latest_by_problem = {}
        for log in logs:
            if log.problem_id not in latest_by_problem:
                latest_by_problem[log.problem_id] = log

        scored = []

        for log in latest_by_problem.values():
            score = 0

            if not log.solved:
                score += 50
            score += (5 - log.confidence) * 10

            scored.append({
                "problem_id": log.problem.id,
                "problem": log.problem.title,
                "pattern": log.problem.pattern.name,
                "confidence": log.confidence,
                "solved": log.solved,
                "priority_score": score,
                "last_attempt": log.created_at,
            })

        scored.sort(key=lambda x: (-x["priority_score"], x["confidence"]))

        return Response(scored[:limit])
