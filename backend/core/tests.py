from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import RecallLog, Topic, Pattern, Problem




class AuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.login_url = reverse("jwt-login")

    def test_login_success_returns_tokens(self):
        response = self.client.post(
            self.login_url,
            {"username": "testuser", "password": "testpass123"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_failure_returns_401(self):
        response = self.client.post(
            self.login_url,
            {"username": "testuser", "password": "wrongpass"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_protected_endpoint_requires_auth(self):
        response = self.client.get("/api/recall-logs/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_protected_endpoint_allows_authenticated_user(self):
        login_response = self.client.post(
            self.login_url,
            {"username": "testuser", "password": "testpass123"},
            format="json"
        )

        token = login_response.data["access"]
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )

        response = self.client.get("/api/recall-logs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)




class RecallLogTests(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            username="recalluser",
            password="recallpass123"
        )


        login_response = self.client.post(
            reverse("jwt-login"),
            {"username": "recalluser", "password": "recallpass123"},
            format="json"
        )

        self.token = login_response.data["access"]
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )


        self.topic = Topic.objects.create(name="Arrays")

        self.pattern = Pattern.objects.create(
            name="Sliding Window",
            topic=self.topic
        )

        self.problem = Problem.objects.create(
            title="Test Problem",
            pattern=self.pattern
        )

        self.recall_logs_url = "/api/recall-logs/"

    def test_create_recall_log(self):
        payload = {
            "problem": self.problem.id,
            "solved": True,
            "confidence": 4,
        }

        response = self.client.post(
            self.recall_logs_url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RecallLog.objects.count(), 1)

    def test_update_recall_log(self):
        log = RecallLog.objects.create(
            user=self.user,
            problem=self.problem,
            solved=False,
            confidence=2,
        )

        response = self.client.patch(
            f"/api/recall-logs/{log.id}/",
            {"confidence": 5},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        log.refresh_from_db()
        self.assertEqual(log.confidence, 5)

    def test_delete_recall_log(self):
        log = RecallLog.objects.create(
            user=self.user,
            problem=self.problem,
            solved=False,
            confidence=2,
        )

        response = self.client.delete(
            f"/api/recall-logs/{log.id}/delete/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(RecallLog.objects.count(), 0)



class AnalyticsSummaryTests(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            username="analyticsuser",
            password="analyticspass123"
        )

        login_response = self.client.post(
            reverse("jwt-login"),
            {"username": "analyticsuser", "password": "analyticspass123"},
            format="json"
        )

        self.token = login_response.data["access"]
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )


        self.topic = Topic.objects.create(name="Arrays")
        self.pattern = Pattern.objects.create(
            name="Sliding Window",
            topic=self.topic
        )
        self.problem = Problem.objects.create(
            title="Test Problem",
            pattern=self.pattern
        )


        RecallLog.objects.create(
            user=self.user,
            problem=self.problem,
            solved=True,
            confidence=4
        )
        RecallLog.objects.create(
            user=self.user,
            problem=self.problem,
            solved=False,
            confidence=2
        )

        self.summary_url = "/api/recall-logs/analytics/summary/"

    def test_summary_values_are_correct(self):
        response = self.client.get(self.summary_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data

        self.assertEqual(data["total_attempts"], 2)
        self.assertEqual(data["solved"], 1)
        self.assertEqual(data["accuracy"], 50)


class AnalyticsWeakPatternsTests(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            username="patternuser",
            password="patternpass123"
        )

        login_response = self.client.post(
            reverse("jwt-login"),
            {"username": "patternuser", "password": "patternpass123"},
            format="json"
        )

        token = login_response.data["access"]
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )


        topic = Topic.objects.create(name="Arrays")

        sliding = Pattern.objects.create(
            name="Sliding Window",
            topic=topic
        )
        hashing = Pattern.objects.create(
            name="Hashing",
            topic=topic
        )

        p1 = Problem.objects.create(title="P1", pattern=sliding)
        p2 = Problem.objects.create(title="P2", pattern=hashing)


        RecallLog.objects.create(
            user=self.user,
            problem=p1,
            solved=False,
            confidence=2
        )
        RecallLog.objects.create(
            user=self.user,
            problem=p1,
            solved=True,
            confidence=4
        )
        RecallLog.objects.create(
            user=self.user,
            problem=p2,
            solved=False,
            confidence=1
        )

        self.url = "/api/recall-logs/analytics/weak-patterns/"

    def test_weak_patterns_aggregation(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data

        # Convert list to dict keyed by pattern name
        patterns = {item["pattern"]: item for item in data}

        self.assertIn("Sliding Window", patterns)
        self.assertIn("Hashing", patterns)

        sliding = patterns["Sliding Window"]
        hashing = patterns["Hashing"]

        # Sliding Window: 2 attempts, 1 solved
        self.assertEqual(sliding["attempts"], 2)
        self.assertEqual(sliding["solved"], 1)
        self.assertEqual(sliding["accuracy"], 50)

        # Hashing: 1 attempt, 0 solved
        self.assertEqual(hashing["attempts"], 1)
        self.assertEqual(hashing["solved"], 0)
        self.assertEqual(hashing["accuracy"], 0)

class AnalyticsWeakProblemsTests(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            username="problemuser",
            password="problempass123"
        )

        login_response = self.client.post(
            reverse("jwt-login"),
            {"username": "problemuser", "password": "problempass123"},
            format="json"
        )

        token = login_response.data["access"]
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )


        topic = Topic.objects.create(name="Arrays")
        pattern = Pattern.objects.create(
            name="Sliding Window",
            topic=topic
        )

        p1 = Problem.objects.create(title="Problem One", pattern=pattern)
        p2 = Problem.objects.create(title="Problem Two", pattern=pattern)


        RecallLog.objects.create(
            user=self.user,
            problem=p1,
            solved=False,
            confidence=2
        )
        RecallLog.objects.create(
            user=self.user,
            problem=p1,
            solved=True,
            confidence=3
        )
        RecallLog.objects.create(
            user=self.user,
            problem=p2,
            solved=False,
            confidence=1
        )

        self.url = "/api/recall-logs/analytics/weak-problems/"

    def test_weak_problems_aggregation(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data

        problems = {item["problem"]: item for item in data}

        self.assertIn("Problem One", problems)
        self.assertIn("Problem Two", problems)

        p1 = problems["Problem One"]
        p2 = problems["Problem Two"]

        # Problem One: 2 attempts, 1 solved
        self.assertEqual(p1["attempts"], 2)
        self.assertEqual(p1["solved"], 1)
        self.assertEqual(p1["accuracy"], 50)

        # Problem Two: 1 attempt, 0 solved
        self.assertEqual(p2["attempts"], 1)
        self.assertEqual(p2["solved"], 0)
        self.assertEqual(p2["accuracy"], 0)


class AnalyticsDailyPlanTests(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            username="dailyuser",
            password="dailypass123"
        )

        login_response = self.client.post(
            reverse("jwt-login"),
            {"username": "dailyuser", "password": "dailypass123"},
            format="json"
        )

        token = login_response.data["access"]
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )


        topic = Topic.objects.create(name="Arrays")
        pattern = Pattern.objects.create(
            name="Sliding Window",
            topic=topic
        )

        p1 = Problem.objects.create(title="High Priority", pattern=pattern)
        p2 = Problem.objects.create(title="Low Priority", pattern=pattern)


        RecallLog.objects.create(
            user=self.user,
            problem=p1,
            solved=False,
            confidence=1
        )

        RecallLog.objects.create(
            user=self.user,
            problem=p2,
            solved=True,
            confidence=5
        )

        self.url = "/api/recall-logs/analytics/daily-plan/"

    def test_daily_plan_ordering(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data

        self.assertGreaterEqual(len(data), 2)

        first = data[0]
        second = data[1]


        self.assertGreaterEqual(
            first["priority_score"],
            second["priority_score"]
        )
