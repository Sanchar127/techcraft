# TechKraft Internal Candidate Scoring System

A full-stack internal tool for managing candidate evaluation, scoring, and AI-assisted review workflows.

Built as part of TechKraft Inc. take-home assignment (Full Stack Engineer - Mid).

---

# 🚀 Tech Stack

### Backend
- FastAPI (Python)
- PostgreSQL
- SQLAlchemy ORM
- JWT Authentication
- Docker

### Frontend
- React (Vite)
- Axios
- Inline CSS styling

### DevOps
- Docker Compose
- PostgreSQL containerized setup

---

# 📦 Features Implemented

## 🔐 Authentication
- JWT-based login system
- Role-based access control (admin / reviewer)
- Reviewer role enforced on registration (no role injection allowed)

---

## 👤 Candidates Module

### Backend APIs
- `GET /candidates`
  - Pagination (skip/limit)
  - Filters: status, role_applied, keyword
- `GET /candidates/{id}`
  - Candidate details
  - Includes scores + AI summary
- `POST /candidates/{id}/scores`
  - Submit score (1–5)
  - Category + optional note
- `POST /candidates/{id}/summary`
  - Mock AI summary (2s async delay)
- `DELETE /candidates/{id}`
  - Soft delete (status → archived)

---

## 🧠 Scoring System
- Reviewers can:
  - Add category-based scores
  - Add notes per score
- Admin can view all scores

---

## 🤖 AI Summary Feature
- Simulated async LLM call using `asyncio.sleep(2)`
- Stores generated summary in DB
- Frontend shows loading + result

---

## 🎨 Frontend Pages

### 1. Login Page
- JWT authentication
- Token stored in localStorage

### 2. Candidate List Page
- Grid view of candidates
- View Details link
- Edit/Delete actions
- Navigation to detail page

### 3. Candidate Detail Page
- Profile info
- AI summary section
- Score submission form
- Score list display

---

## 🐘 Database Design

### Candidates Table
- id (UUID)
- name
- email
- role_applied
- status (new/reviewed/hired/rejected/archived)
- skills (array)
- internal_notes (admin only)
- created_at
- deleted_at (soft delete)

### Scores Table
- id (UUID)
- candidate_id
- reviewer_id
- category
- score (1–5)
- note
- created_at

---

## ⚙️ Docker Setup

### Services
- PostgreSQL (port 5432)
- Backend FastAPI (port 8000)
- Frontend Vite (port 5173)

### Run project
```bash
docker-compose up --build








🧠 Architecture Decision Records (ADR)
ADR 1: PostgreSQL over SQLite

Context: Need relational structure for candidates and scores with filtering and indexing.

Decision: Used PostgreSQL via Docker Compose.

Trade-off: Slightly heavier setup than SQLite but provides scalability and production readiness.

ADR 2: Soft Delete Strategy

Context: Candidates should not be permanently removed.

Decision: Implemented soft delete using deleted_at and status = "archived".

Trade-off: Slightly larger dataset but ensures data traceability.

ADR 3: JWT Authentication

Context: Need secure role-based access for reviewers and admins.

Decision: Used JWT tokens with role embedded.

Trade-off: Stateless system (no session tracking), but scalable and simple.

ADR 4: Mock AI Summary

Context: No real LLM integration required.

Decision: Used asyncio.sleep(2) to simulate AI processing.

Trade-off: No real AI intelligence but demonstrates async handling correctly.

🐛 Debugging Signal (Important Fix)
Problem in given snippet:
all_candidates = db.execute("SELECT * FROM candidates").fetchall()
filtered = [c for c in all_candidates if c["status"] == status]
❌ Issues:
Loads entire dataset into memory
Filters in Python instead of DB
Breaks pagination efficiency
Not scalable for large datasets
✅ Correct approach:
Push filtering to database
Use indexed SQL queries

Example fix:

SELECT * FROM candidates
WHERE status = :status
AND name ILIKE :keyword
LIMIT :limit OFFSET :offset;
📈 Learning Reflection

During this project, I implemented role-based access control with JWT and built a full-stack scoring workflow between reviewers and candidates. If given more time, I would explore integrating real-time updates using WebSockets or SSE for live score tracking across reviewers.

⚠️ Known Limitations
No real AI model integration (mocked summary)
No WebSocket/SSE real-time updates implemented
Basic UI styling (no design system used)
No unit tests included due to time constraint (can be added next)
📦 API Examples
Login
POST /auth/login
Get candidates
GET /candidates?skip=0&limit=20
Add score
POST /candidates/{id}/scores?category=backend&score=4&note=good
Generate summary
POST /candidates/{id}/summary
📁 Project Structure
backend/
  app/
    models.py
    routers/
    auth.py
    main.py

frontend/
  src/
    pages/
    components/

docker-compose.yml
README.md
✅ How to Run
docker-compose up --build

Frontend:

http://localhost:5173

Backend:

http://localhost:8000/docs
🎯 Final Note

This project demonstrates:

Full-stack API design
Role-based authentication
Candidate scoring workflow
Async processing simulation
Dockerized microservice setupa

---



