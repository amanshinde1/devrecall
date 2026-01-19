#api_urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .api_views import (
    TopicListAPIView,
    PatternListAPIView,
    ProblemListAPIView,
    RecallLogListCreateAPIView,
    RecallLogUpdateAPIView,
    RecallLogDeleteAPIView,
    RecallSummaryAPIView,
)

urlpatterns = [
    path('topics/', TopicListAPIView.as_view(), name='api-topics'),
    path('patterns/', PatternListAPIView.as_view(), name='api-patterns'),
    path('problems/', ProblemListAPIView.as_view(), name='api-problems'),
    path('recall-logs/', RecallLogListCreateAPIView.as_view(), name='api-recall-logs'),
    path(
        'recall-logs/<int:pk>/',
        RecallLogUpdateAPIView.as_view(),
        name='api-recall-log-update',
    ),
    path(
        "recall-logs/<int:pk>/delete/",
        RecallLogDeleteAPIView.as_view(),
        name="api-recall-log-delete",
    ),
    path('auth/login/', TokenObtainPairView.as_view(), name='jwt-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
    path(
    "recall-logs/analytics/summary/",
    RecallSummaryAPIView.as_view(),
    name="api-recall-summary",
),



]
