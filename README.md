# LinkedInCareerPilot AI 🚀

> **Your AI-Powered LinkedIn & Career Growth Assistant.**  
> A production-ready, multi-tenant SaaS platform that unifies job discovery, AI job description matching, LinkedIn technical thought-leadership content generation, GitHub repository monitoring, application pipeline tracking, and career analytics.

[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.18-red?style=for-the-badge)](https://www.django-rest-framework.org/)
[![React](https://img.shields.io/badge/React-18.3-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.5-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

---

## 🎯 Architecture & Design

LinkedInCareerPilot AI follows a **human-in-the-loop, zero-trust multi-tenant SaaS architecture**. Autonomous AI agents assist with research, JD parsing, and content drafting, while sensitive actions (submitting applications, publishing posts) remain under user review.

```text
                                  CLIENT BROWSERS
                                         │
                                         ▼
                                   NGINX REVERSE PROXY
                         (Port 80 - Static SPA + Proxy Routing)
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 │                                               │
                 ▼                                               ▼
         REACT FRONTEND (SPA)                           DJANGO REST API
     React Router v6 + Axios + Vite              (Port 8000 - Gunicorn WSGI)
                 │                                               │
                 │                                               ▼
                 │                                  ┌─────────────────────────┐
                 │                                  │  JWT Auth & Permissions │
                 │                                  │  Strict Tenant Isolation│
                 │                                  │  Service Layer          │
                 │                                  └────────────┬────────────┘
                 │                                               │
                 └─────────────── API Requests ──────────────────┼────────────────┐
                                                                 ▼                ▼
                                                            PostgreSQL /        Redis
                                                              SQLite3        (Cache & Celery)
```

---

## ✨ Core Pillars

1. **AI Job Hunter**: High-match score evaluation, keyword and transferable skill extraction, gap identification, and employment mode filtering (Remote, Hybrid, On-site).
2. **LinkedIn Content Agent**: Post generator with 5 distinct tones (`Professional`, `Thought Leadership`, `Storytelling`, `Educational`, `Casual`), review pipeline (`Draft` -> `Approved` -> `Published`), and performance metrics.
3. **Profile Guardian**: Multi-dimensional profile health audit (Headline, About, Skills, Projects, GitHub) with actionable recommendations.
4. **GitHub Career Monitor**: Connects public repositories, tracks activity milestones (e.g. distributed queue implementations), and drafts content ideas from code commits.
5. **Application Pipeline**: Kanban-style tracker tracking stages: `Saved` -> `Applied` -> `Interview` -> `Offer` -> `Rejected`.
6. **AI Agent Orchestration**: 6 autonomous agents (`Job Hunter`, `Job Analyzer`, `Content Writer`, `Profile Guardian`, `GitHub Monitor`, `Career Analyst`) with integrated AI credit tracking.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python 3.12, Django 5.2, Django REST Framework, SimpleJWT, Celery, Redis, Gunicorn |
| **Frontend** | React 18, React Router v6, Axios, Vite, Tailwind CSS, Lucide Icons |
| **Database** | Development: SQLite3 (zero-config) • Production: PostgreSQL 16 |
| **Documentation**| OpenAPI 3.0 & Interactive Swagger UI (`drf-spectacular`) |
| **DevOps** | Docker, Docker Compose, Nginx, Gunicorn, AWS EC2 ready |

---

## 🚀 Quick Start Guide

### 1. Prerequisites

- Python 3.12+
- Node.js 18+ and npm
- Git
- *(Optional)* Docker and Docker Compose

---

### 2. Local Development Setup

#### Backend Setup

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/linkedin-career-pilot-ai.git
cd linkedin-career-pilot-ai

# 2. Configure environment
cp .env.example .env

# 3. Create and activate virtual environment
python3 -m venv backend/venv
source backend/venv/bin/activate   # On Windows: backend\venv\Scripts\activate

# 4. Install backend dependencies
pip install -r backend/requirements.txt

# 5. Apply database migrations
python backend/manage.py migrate

# 6. Seed demonstration data (Creates demo user, tenant, jobs, posts, agents)
python backend/manage.py seed_data

# 7. Start Django development server
python backend/manage.py runserver 127.0.0.1:8000
```

> **Demo Credentials created by `seed_data`**:
> - **Email**: `demo@linkedincareerpilot.ai`
> - **Password**: `Password123!`

#### Frontend Setup

In a new terminal window:

```bash
cd frontend

# 1. Install dependencies
npm install

# 2. Start development server
npm run dev
```

Visit **`http://localhost:5173`** in your browser.

---

### 3. Docker Compose Setup (Production Simulation)

Run the full stack (PostgreSQL + Redis + Django/Gunicorn + React/Nginx) with a single command:

```bash
docker compose up --build -d
```

- **Frontend App**: `http://localhost`
- **Backend API**: `http://localhost/api/v1/`
- **API Documentation**: `http://localhost/api/docs/`
- **Django Admin**: `http://localhost/admin/`

To populate demo data inside the Docker container:

```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_data
```

---

## 📖 API Documentation & Endpoints

Interactive Swagger & OpenAPI documentation is available out of the box:

- **Swagger UI**: `http://127.0.0.1:8000/api/docs/`
- **OpenAPI Schema (JSON/YAML)**: `http://127.0.0.1:8000/api/schema/`
- **ReDoc**: `http://127.0.0.1:8000/api/redoc/`

### Primary REST Endpoints:

| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/auth/login/` | `POST` | Authenticate user & receive JWT access + refresh tokens |
| `/api/v1/auth/register/` | `POST` | Register user & provision default tenant workspace |
| `/api/v1/auth/me/` | `GET` | Get current user, tenant, and role |
| `/api/v1/dashboard/` | `GET` | Aggregated career KPIs and pipeline metrics |
| `/api/v1/jobs/` | `GET` | Search jobs with work_mode and keyword filters |
| `/api/v1/jobs/{id}/analyze/` | `POST` | Run AI match evaluation against user profile |
| `/api/v1/jobs/{id}/save_job/` | `POST` | Save job to Application Tracker |
| `/api/v1/applications/` | `GET` | List applications filtered by status |
| `/api/v1/applications/{id}/update_status/` | `PATCH` | Update stage (`SAVED`, `APPLIED`, `INTERVIEW`, `OFFER`) |
| `/api/v1/content/` | `GET` | List generated LinkedIn posts |
| `/api/v1/content/generate/` | `POST` | Generate AI LinkedIn post for given topic & tone |
| `/api/v1/content/{id}/approve/` | `POST` | Approve draft for publishing |
| `/api/v1/profile/health/` | `GET` | Profile Health audit scores and suggestions |
| `/api/v1/github/repositories/` | `GET` | List tracked GitHub repositories |
| `/api/v1/github/repositories/sync/`| `POST` | Trigger repository & activity synchronization |
| `/api/v1/agents/` | `GET` | List available autonomous AI agents |
| `/api/v1/agents/{id}/run/` | `POST` | Execute agent task and consume credits |
| `/api/v1/subscriptions/plans/` | `GET` | List available subscription tiers |

---

## 🧪 Testing

Run backend automated test suite:

```bash
python backend/manage.py test api
```

Run frontend typecheck and production build:

```bash
cd frontend
npm run lint
npm run build
```

---

## 📂 Project Structure

```text
linkedin-career-pilot-ai/
├── backend/                        # Django REST API
│   ├── accounts/                   # Auth, Users, OAuth
│   ├── tenants/                    # Multi-tenancy & membership
│   ├── profiles/                   # User profiles, skills, snapshots
│   ├── jobs/                       # Job ingestion, matching, analyses
│   ├── applications/               # Application pipeline, interviews
│   ├── content/                    # LinkedIn posts, performance
│   ├── github/                     # GitHub repositories & activity
│   ├── agents/                     # AI agents & execution engine
│   ├── subscriptions/              # Plans, tiers, credits
│   ├── billing/                    # Invoices, payments, webhooks
│   ├── notifications/              # In-app, telegram, email alerts
│   ├── analytics/                  # Career metrics & insights
│   ├── api/                        # Shared API views & seed command
│   ├── core/                       # Django project settings & URLs
│   ├── requirements.txt            # Python dependencies
│   └── manage.py                   # Django CLI
│
├── frontend/                       # React.js SPA
│   ├── src/
│   │   ├── components/layout/      # Sidebar, TopBar, ProtectedRoute
│   │   ├── context/                # AuthContext (JWT management)
│   │   ├── pages/                  # Route views (Dashboard, Jobs, etc.)
│   │   ├── services/               # Axios API client with interceptors
│   │   ├── types/                  # TypeScript interfaces
│   │   ├── App.tsx                 # React Router v6 routing
│   │   └── main.tsx                # Application entrypoint
│   ├── index.html                  # HTML5 shell
│   ├── vite.config.ts              # Vite bundler configuration
│   ├── tailwind.config.js          # Tailwind CSS theme
│   └── package.json                # NPM dependencies
│
├── docker/                         # Docker & Nginx infrastructure
│   ├── Dockerfile.backend          # Python 3.12 WSGI image
│   ├── Dockerfile.frontend         # Multi-stage React + Nginx image
│   └── nginx.conf                  # Nginx reverse proxy configuration
│
├── docker-compose.yml              # Production container orchestration
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
└── README.md                       # Documentation
```

---

## 🔐 Security & Multi-Tenancy

- **JWT Authentication**: Short-lived access tokens with rotating refresh tokens via `djangorestframework-simplejwt`.
- **Zero-Trust Multi-Tenancy**: Every data query is scoped strictly through authenticated user session context:
  ```python
  Job.objects.filter(tenant=request.user.tenant)
  ```
- **CORS Protection**: Controlled allowed origins across local and production domains.
- **Environment Isolation**: Secrets, credentials, and API keys are strictly loaded via `.env` and excluded from version control.

---

## 📜 License

This project is licensed under the MIT License.
