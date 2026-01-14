from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Topic, Pattern, Problem, RecallLog
from .serializers import (
    TopicSerializer,
    PatternSerializer,
    ProblemSerializer,
    RecallLogSerializer,
)


class TopicListAPIView(ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class PatternListAPIView(ListAPIView):
    serializer_class = PatternSerializer

    def get_queryset(self):
        queryset = Pattern.objects.select_related('topic').all()
        topic_id = self.request.query_params.get('topic')
        if topic_id:
            queryset = queryset.filter(topic_id=topic_id)
        return queryset.order_by('name')


class ProblemListAPIView(ListAPIView):
    queryset = Problem.objects.select_related('pattern').all()
    serializer_class = ProblemSerializer


class RecallLogListCreateAPIView(ListAPIView, CreateAPIView):
    queryset = RecallLog.objects.select_related("problem", "user").order_by("-created_at")
    serializer_class = RecallLogSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
