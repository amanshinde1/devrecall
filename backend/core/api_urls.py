from django.urls import path
from .api_views import (
    TopicListAPIView,
    PatternListAPIView,
    ProblemListAPIView,
    RecallLogListAPIView,
)

urlpatterns = [
    path('topics/', TopicListAPIView.as_view(), name='api-topics'),
    path('patterns/', PatternListAPIView.as_view(), name='api-patterns'),
    path('problems/', ProblemListAPIView.as_view(), name='api-problems'),
    path('recall-logs/', RecallLogListAPIView.as_view(), name='api-recall-logs'),
]
