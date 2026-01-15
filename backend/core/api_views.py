from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

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
# RECALL LOG APIs
# --------------------

class RecallLogListCreateAPIView(ListAPIView, CreateAPIView):
    """
    GET  /api/recall-logs/
    POST /api/recall-logs/
    """
    serializer_class = RecallLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecallLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecallLogUpdateAPIView(RetrieveUpdateAPIView):
    """
    PUT / PATCH /api/recall-logs/<id>/
    """
    serializer_class = RecallLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecallLog.objects.filter(user=self.request.user)


class RecallLogDeleteAPIView(DestroyAPIView):
    """
    DELETE /api/recall-logs/<id>/
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecallLog.objects.filter(user=self.request.user)
