# DevRecall — Backend System

DevRecall is a backend-first system designed to help software engineers
retain **Data Structures & Algorithms (DSA)** knowledge through
structured recall tracking and data-driven revision.

Instead of focusing on task completion or streaks, DevRecall models
**how well a problem was recalled**, **how confident the user was**, and
**when it should be revised again**.

This repository represents a **complete backend implementation**.

---

## Problem Statement

During long DSA preparation cycles, developers often:
- Solve problems correctly once
- Forget patterns weeks later
- Relearn the same concepts repeatedly

DevRecall addresses this by answering one question:

> *What should I revise next, and why?*

---

## Core Domain Model

DevRecall is built around four core entities:

- **Topic**  
  High-level DSA categories (Arrays, Trees, Graphs)

- **Pattern**  
  Reusable problem-solving techniques (Sliding Window, Two Pointers)

- **Problem**  
  Individual DSA problems, either system-defined or user-owned

- **RecallLog**  
  A single recall attempt capturing:
  - solved / unsolved outcome
  - confidence score (1–5)
  - notes
  - derived review priority

This model allows the system to reason about **recall quality**, not just problem counts.

---

## Key Backend Capabilities

- JWT-based authentication (access & refresh tokens)
- User-scoped data ownership and isolation
- Recall logging with confidence-based scoring
- Automatic review scheduling logic
- Analytics endpoints for:
  - recall accuracy
  - weak patterns
  - weak problems
  - review queues
  - daily revision plans
- Clean REST API design using Django REST Framework
- Production-aware schema design (PostgreSQL-ready)

---

## Tech Stack

| Layer | Technology |
|-----|-----------|
| Language | Python |
| Framework | Django |
| API | Django REST Framework |
| Auth | SimpleJWT |
| Database | SQLite (development) |
| ORM | Django ORM |
| Tooling | Django Admin, Django Migrations |

The backend is intentionally **database-agnostic** and can be deployed
with PostgreSQL without schema changes.

---

## Project Structure

```text
devrecall/
├── backend/
│   ├── backend/
│   ├── core/
│   │   ├── models.py
│   │   ├── api_views.py
│   │   ├── serializers.py
│   │   ├── api_urls.py
│   │   └── tests.py
│   ├── manage.py
│   └── db.sqlite3
└── README.md
```
---

## Author

Aman Shinde  
Backend Developer — Python & Django
