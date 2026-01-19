# api_urls.py
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
    RecallWeakPatternsAPIView,
    RecallWeakProblemsAPIView,
    RecallReviewQueueAPIView,
    RecallDailyPlanAPIView,
)

urlpatterns = [
    # --------------------
    # CORE READ APIs
    # --------------------
    path("topics/", TopicListAPIView.as_view(), name="api-topics"),
    path("patterns/", PatternListAPIView.as_view(), name="api-patterns"),
    path("problems/", ProblemListAPIView.as_view(), name="api-problems"),

    # --------------------
    # RECALL LOG CRUD
    # --------------------
    path(
        "recall-logs/",
        RecallLogListCreateAPIView.as_view(),
        name="api-recall-logs",
    ),
    path(
        "recall-logs/<int:pk>/",
        RecallLogUpdateAPIView.as_view(),
        name="api-recall-log-update",
    ),
    path(
        "recall-logs/<int:pk>/delete/",
        RecallLogDeleteAPIView.as_view(),
        name="api-recall-log-delete",
    ),

    # --------------------
    # AUTH (JWT)
    # --------------------
    path("auth/login/", TokenObtainPairView.as_view(), name="jwt-login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("auth/verify/", TokenVerifyView.as_view(), name="jwt-verify"),

    # --------------------
    # RECALL INTELLIGENCE
    # --------------------
    path(
        "recall-logs/analytics/summary/",
        RecallSummaryAPIView.as_view(),
        name="api-recall-summary",
    ),
    path(
        "recall-logs/analytics/weak-patterns/",
        RecallWeakPatternsAPIView.as_view(),
        name="api-recall-weak-patterns",
    ),
    path(
        "recall-logs/analytics/weak-problems/",
        RecallWeakProblemsAPIView.as_view(),
        name="api-recall-weak-problems",
    ),
    path(
        "recall-logs/analytics/review-queue/",
        RecallReviewQueueAPIView.as_view(),
        name="api-recall-review-queue",
    ),
    path(
        "recall-logs/analytics/daily-plan/",
        RecallDailyPlanAPIView.as_view(),
        name="api-daily-plan",
    ),
]
