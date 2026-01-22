from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.contrib.auth.models import User
from django.db.models import Count, Avg, Q

from .models import Topic, Pattern, Problem, RecallLog
from .serializers import (
    TopicSerializer,
    PatternSerializer,
    ProblemSerializer,
    RecallLogSerializer,
)


class RegisterAPIView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        User.objects.create_user(username=username, password=password)

        return Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED,
        )



class TopicListAPIView(ListAPIView):
    queryset = Topic.objects.all().order_by("name")
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
    serializer_class = ProblemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Problem.objects
            .filter(Q(user__isnull=True) | Q(user=self.request.user))
            .select_related("pattern", "pattern__topic")
            .order_by("pattern__topic__name", "pattern__name", "title")
        )


class ProblemCreateAPIView(CreateAPIView):
    serializer_class = ProblemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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



class RecallSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = RecallLog.objects.filter(user=request.user)

        total_attempts = logs.count()
        solved_count = logs.filter(solved=True).count()
        accuracy = (
            round((solved_count / total_attempts) * 100, 2)
            if total_attempts
            else 0
        )

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
                "avg_confidence": round(item["avg_confidence"], 2)
                if item["avg_confidence"] else 0,
            })

        response.sort(key=lambda x: x["accuracy"])
        return Response(response)


class RecallWeakProblemsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = (
            RecallLog.objects
            .filter(user=request.user)
            .values(
                "problem__id",
                "problem__title",
                "problem__pattern__name"
            )
            .annotate(
                attempts=Count("id"),
                solved=Count("id", filter=Q(solved=True)),
                avg_confidence=Avg("confidence"),
            )
        )

        weak = []
        for item in logs:
            attempts = item["attempts"]
            solved = item["solved"]
            accuracy = round((solved / attempts) * 100, 2) if attempts else 0
            avg_conf = round(item["avg_confidence"], 2) if item["avg_confidence"] else 0

            if accuracy < 70 or avg_conf <= 3:
                weak.append({
                    "problem_id": item["problem__id"],
                    "problem": item["problem__title"],
                    "pattern": item["problem__pattern__name"],
                    "attempts": attempts,
                    "solved": solved,
                    "accuracy": accuracy,
                    "avg_confidence": avg_conf,
                })

        weak.sort(key=lambda x: (x["accuracy"], x["avg_confidence"]))
        return Response(weak)


class RecallReviewQueueAPIView(APIView):
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
                "confidence": log.confidence,
                "solved": log.solved,
                "last_attempt": log.created_at,
            })

        return Response(queue)


class RecallDailyPlanAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        limit = int(request.query_params.get("limit", 5))

        logs = (
            RecallLog.objects
            .filter(user=request.user)
            .select_related("problem", "problem__pattern")
            .order_by("-created_at")
        )

        latest = {}
        for log in logs:
            if log.problem_id not in latest:
                latest[log.problem_id] = log

        scored = []
        for log in latest.values():
            score = (5 - log.confidence) * 10
            if not log.solved:
                score += 50

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


class RecallHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = (
            RecallLog.objects
            .filter(user=request.user)
            .select_related(
                "problem",
                "problem__pattern",
                "problem__pattern__topic",
            )
            .order_by("-created_at")
        )

        data = []
        for log in logs:
            data.append({
                "id": log.id,
                "problem_id": log.problem.id,
                "problem": log.problem.title,
                "pattern": log.problem.pattern.name,
                "topic": log.problem.pattern.topic.name,
                "confidence": log.confidence,
                "solved": log.solved,
                "notes": log.notes or "",
                "created_at": log.created_at,

                "next_review_at": log.next_review_at,
                "priority_score": log.priority_score,
            })

        return Response(data)
