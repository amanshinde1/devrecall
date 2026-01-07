DevRecall – Backend

DevRecall is a backend system designed to help software engineers retain and revise Data Structures & Algorithms concepts through structured recall and practice tracking.

The project focuses on solving a common problem during long DSA preparation cycles: forgetting patterns and mistakes over time despite regular practice.

This repository contains Backend V1, which includes the complete data model, database migrations, and admin tooling.

Core Concepts

DevRecall is built around four core entities:

Topic – High-level DSA categories such as Arrays, Stacks, Trees, etc.

Pattern – Problem-solving techniques under a topic, such as Sliding Window or Two Pointers

Problem – Individual DSA problems linked to a pattern

RecallLog – Records each practice attempt along with outcome and confidence level

This structure enables tracking what was practiced, how well it was solved, and when it should be revised again.

Tech Stack

Backend: Python, Django

Database: SQLite (development)

ORM: Django ORM

Admin Tooling: Django Admin

Version Control: Git, GitHub

The project is designed to be database-agnostic and can be migrated to PostgreSQL for production use.

Features (Backend V1)

Relational data modeling using Django ORM

Proper foreign-key relationships and constraints

Database migrations

Django Admin integration for data inspection and testing

Verified end-to-end data flow (Topic → Pattern → Problem → RecallLog)

Project Structure
devrecall/
├── backend/
│   ├── backend/        # project settings and configuration
│   ├── core/           # core domain logic and models
│   ├── manage.py
│   └── db.sqlite3      # local development database (ignored in Git)
└── README.md

Local Setup

Clone the repository and navigate into it

Create and activate a virtual environment

Install Django

Run database migrations

Create a superuser

Start the development server

Access Django Admin at http://127.0.0.1:8000/admin

Current Status

Backend V1 is completed.

Planned next phases include:

REST API layer using Django REST Framework

PostgreSQL integration

Authentication-protected endpoints

Recall analytics and spaced repetition logic

Author

Aman Shinde
Backend Developer (Python, Django)