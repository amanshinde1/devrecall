from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .api_views import (
    RegisterAPIView,
    TopicListAPIView,
    PatternListAPIView,
    ProblemListAPIView,
    ProblemCreateAPIView,
    RecallLogListCreateAPIView,
    RecallLogUpdateAPIView,
    RecallLogDeleteAPIView,
    RecallSummaryAPIView,
    RecallWeakPatternsAPIView,
    RecallWeakProblemsAPIView,
    RecallReviewQueueAPIView,
    RecallDailyPlanAPIView,
    RecallHistoryAPIView,

)

urlpatterns = [
    path("auth/login/", TokenObtainPairView.as_view(), name="jwt-login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("auth/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    path("auth/register/", RegisterAPIView.as_view(), name="register"),
    path("topics/", TopicListAPIView.as_view(), name="api-topics"),
    path("patterns/", PatternListAPIView.as_view(), name="api-patterns"),
    path("problems/", ProblemListAPIView.as_view(), name="api-problems"),
    path("problems/create/", ProblemCreateAPIView.as_view(), name="api-problem-create"),
    path("recall-logs/", RecallLogListCreateAPIView.as_view(), name="api-recall-logs"),
    path("recall-logs/<int:pk>/", RecallLogUpdateAPIView.as_view(), name="api-recall-log-update"),
    path("recall-logs/<int:pk>/delete/", RecallLogDeleteAPIView.as_view(), name="api-recall-log-delete"),
    path("recall-logs/analytics/summary/", RecallSummaryAPIView.as_view(), name="api-recall-summary"),
    path("recall-logs/analytics/weak-patterns/", RecallWeakPatternsAPIView.as_view(), name="api-recall-weak-patterns"),
    path("recall-logs/analytics/weak-problems/", RecallWeakProblemsAPIView.as_view(), name="api-recall-weak-problems"),
    path("recall-logs/analytics/review-queue/", RecallReviewQueueAPIView.as_view(), name="api-recall-review-queue"),
    path("recall-logs/analytics/daily-plan/", RecallDailyPlanAPIView.as_view(), name="api-daily-plan"),
    path("recall-logs/history/", RecallHistoryAPIView.as_view(), name="api-recall-history"),

]
