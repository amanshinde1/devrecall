from django.core.management.base import BaseCommand
from core.models import Topic, Pattern, Problem


class Command(BaseCommand):
    help = "Seed system DSA topics, patterns, and problems (idempotent)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Seeding DSA data..."))

        # =========================
        # TOPICS
        # =========================
        topics = {
            "Arrays": {},
            "Strings": {},
            "Linked Lists": {},
            "Stacks & Queues": {},
            "Trees": {},
            "Graphs": {},
            "Dynamic Programming": {},
            "Greedy": {},
            "Binary Search": {},
        }

        topic_objs = {}
        for name in topics:
            obj, _ = Topic.objects.get_or_create(name=name)
            topic_objs[name] = obj

        # =========================
        # PATTERNS
        # =========================
        patterns = {
            "Arrays": [
                ("Sliding Window", "Window-based subarray problems"),
                ("Two Pointers", "Use two indices to converge"),
                ("Prefix Sum", "Precompute cumulative sums"),
            ],
            "Strings": [
                ("Sliding Window", "Substring window techniques"),
                ("Frequency Map", "Character counting"),
            ],
            "Linked Lists": [
                ("Fast & Slow Pointers", "Cycle detection / mid"),
            ],
            "Stacks & Queues": [
                ("Monotonic Stack", "Next greater/smaller element"),
            ],
            "Trees": [
                ("DFS", "Depth-first traversal"),
                ("BFS", "Level-order traversal"),
            ],
            "Graphs": [
                ("BFS", "Shortest paths (unweighted)"),
                ("DFS", "Traversal & components"),
            ],
            "Dynamic Programming": [
                ("1D DP", "Linear DP"),
                ("2D DP", "Grid / sequence DP"),
            ],
            "Greedy": [
                ("Greedy Choice", "Local optimal decisions"),
            ],
            "Binary Search": [
                ("Binary Search on Answer", "Search solution space"),
            ],
        }

        pattern_objs = {}

        for topic_name, plist in patterns.items():
            topic = topic_objs[topic_name]
            for pname, desc in plist:
                p, _ = Pattern.objects.get_or_create(
                    name=pname,
                    topic=topic,
                    defaults={"description": desc},
                )
                pattern_objs[(topic_name, pname)] = p

        # =========================
        # SYSTEM PROBLEMS
        # =========================
        problems = [
            # Arrays / Sliding Window
            ("Maximum Subarray Sum of Size K", "Arrays", "Sliding Window", "easy",
             "https://leetcode.com/problems/maximum-average-subarray-i/"),
            ("Longest Substring Without Repeating Characters", "Strings", "Sliding Window", "medium",
             "https://leetcode.com/problems/longest-substring-without-repeating-characters/"),

            # Arrays / Two Pointers
            ("Two Sum (Sorted Array)", "Arrays", "Two Pointers", "easy",
             "https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/"),

            # Prefix Sum
            ("Subarray Sum Equals K", "Arrays", "Prefix Sum", "medium",
             "https://leetcode.com/problems/subarray-sum-equals-k/"),

            # Linked List
            ("Detect Cycle in Linked List", "Linked Lists", "Fast & Slow Pointers", "easy",
             "https://leetcode.com/problems/linked-list-cycle/"),

            # Stack
            ("Next Greater Element", "Stacks & Queues", "Monotonic Stack", "medium",
             "https://leetcode.com/problems/next-greater-element-i/"),

            # Tree
            ("Binary Tree Level Order Traversal", "Trees", "BFS", "medium",
             "https://leetcode.com/problems/binary-tree-level-order-traversal/"),
            ("Maximum Depth of Binary Tree", "Trees", "DFS", "easy",
             "https://leetcode.com/problems/maximum-depth-of-binary-tree/"),

            # Graph
            ("Number of Islands", "Graphs", "DFS", "medium",
             "https://leetcode.com/problems/number-of-islands/"),

            # DP
            ("Climbing Stairs", "Dynamic Programming", "1D DP", "easy",
             "https://leetcode.com/problems/climbing-stairs/"),

            # Binary Search
            ("Search in Rotated Sorted Array", "Binary Search", "Binary Search on Answer", "medium",
             "https://leetcode.com/problems/search-in-rotated-sorted-array/"),
        ]

        created = 0
        for title, topic, pattern, difficulty, link in problems:
            ptn = pattern_objs[(topic, pattern)]

            _, was_created = Problem.objects.get_or_create(
                title=title,
                pattern=ptn,
                difficulty=difficulty,
                defaults={
                    "external_link": link,
                    "user": None,  # SYSTEM OWNED
                }
            )

            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"DSA seed completed successfully. New problems added: {created}"
            )
        )
