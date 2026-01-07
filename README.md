# 🚀 DevRecall – Backend

**DevRecall** is a backend system designed to help software engineers retain and revise **Data Structures & Algorithms (DSA)** concepts through structured recall and practice tracking.

The project addresses a common issue during long DSA preparation cycles: forgetting problem-solving patterns and recurring mistakes over time despite regular practice.

This repository contains **Backend V1**, which focuses on core data modeling, migrations, and admin tooling.

---

## Tech Stack

| Component | Technology |
|---------|------------|
| Language | Python |
| Framework | Django |
| Database | SQLite (development) |
| ORM | Django ORM |
| Tooling | Django Admin, Git |

The system is designed to be **database-agnostic** and can be migrated to PostgreSQL for production environments.

---

## Core Concepts

DevRecall is built around four core domain entities:

- **Topic** – High-level DSA categories such as Arrays, Stacks, Trees, etc.
- **Pattern** – Problem-solving techniques under a topic (e.g., Sliding Window, Two Pointers).
- **Problem** – Individual DSA problems linked to a specific pattern.
- **RecallLog** – Records each practice attempt along with outcome and confidence level.

This structure enables tracking **what was practiced, how well it was solved, and when it should be revised again**.

---

## Features (Backend V1)

- Relational data modeling using Django ORM  
- Proper foreign-key relationships and constraints  
- Version-controlled database migrations  
- Django Admin integration for inspection and testing  
- Verified end-to-end data flow  
  (Topic → Pattern → Problem → RecallLog)  
- Production-aware schema design (PostgreSQL-ready)

---

## Project Structure

```text
devrecall/
├── backend/
│   ├── backend/        
│   ├── core/           
│   ├── manage.py       
│   └── db.sqlite3      
└── README.md
```


---

## Local Setup

1. Clone the repository and navigate into it  
2. Create and activate a virtual environment  
3. Install Django  
4. Run database migrations  
5. Create a superuser  
6. Start the development server  
7. Access Django Admin at  
   http://127.0.0.1:8000/admin

---

## Current Status & Roadmap

**Backend V1 is completed.**

Planned next phases:

- REST API layer using Django REST Framework  
- PostgreSQL integration  
- Authentication-protected endpoints  
- Recall analytics and spaced repetition logic  

---

## Author

**Aman Shinde**  
Backend Developer (Python, Django)  
GitHub • LinkedIn
