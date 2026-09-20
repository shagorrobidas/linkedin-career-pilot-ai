# LinkedInCareerPilot AI — System Design

> **Technical architecture and system design specification**

---

# 1. Overview

LinkedInCareerPilot AI is a **multi-tenant SaaS + AI Agent platform** designed to help professionals manage their LinkedIn presence, discover career opportunities, monitor professional activity, track applications, and receive AI-powered career recommendations.

The system is built around:

```text
Next.js
   ↓
Django REST Framework
   ↓
Service Layer
   ↓
PostgreSQL + Redis
   ↓
Celery Workers
   ↓
AI Providers + External APIs
```

---

# 2. Architecture

```text
                           INTERNET
                              │
                              ▼
                           NGINX
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
             NEXT.JS UI               API CLIENTS
                 │                         │
                 └────────────┬────────────┘
                              ▼
                       DJANGO REST API
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
 Authentication          Tenant Layer          Permissions
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
                         SERVICE LAYER
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
       ▼                      ▼                      ▼
   PostgreSQL              Redis                 External APIs
       │                      │                      │
       │                      ▼                      ├── GitHub
       │                 Celery Queue               ├── Job Sources
       │                      │                      ├── AI Providers
       │                      ▼                      └── Notifications
       │                Celery Workers
       │                      │
       │                      ▼
       │                AI Orchestrator
       │                      │
       └──────────────────────┘
```

---

# 3. Multi-Tenancy

Every business object should be associated with a tenant.

```text
User
  ↓
Tenant
  ↓
Tenant-owned resources
```

Example:

```python
Job.objects.filter(
    tenant=request.tenant
)
```

Never trust a client-provided `tenant_id`.

The tenant should be resolved from authenticated context.

---

# 4. Tenant Isolation

The request lifecycle should enforce:

```text
HTTP Request
     ↓
Authentication
     ↓
User Resolution
     ↓
Tenant Resolution
     ↓
Permission Check
     ↓
Tenant-scoped Query
     ↓
Business Logic
```

Every relevant query must be tenant-aware.

---

# 5. Roles

Initial roles:

```text
OWNER
ADMIN
MEMBER
```

Future:

```text
CAREER_COACH
RECRUITER
TEAM_MEMBER
```

Permissions should follow:

```text
Tenant
  ↓
Role
  ↓
Permission
  ↓
Object
```

---

# 6. AI Agent Architecture

The AI system uses a central orchestrator.

```text
                         AI ORCHESTRATOR
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
   JOB HUNTER              CONTENT AGENT          PROFILE AGENT
        │                       │                       │
        ▼                       ▼                       ▼
 JOB ANALYZER              TOPIC ENGINE          GITHUB AGENT
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                ▼
                         CAREER ANALYST
                                │
                                ▼
                        RECOMMENDATIONS
```

---

# 7. Agent Lifecycle

```text
REQUESTED
   ↓
QUEUED
   ↓
RUNNING
   ↓
AI PROCESSING
   ↓
VALIDATING
   ↓
COMPLETED
```

Failure:

```text
RUNNING
   ↓
FAILED
   ↓
RETRY
   ↓
RUNNING
```

Agent executions should store:

- Input
- Context
- Agent
- Provider
- Model
- Output
- Tokens
- Credits
- Duration
- Status
- Error
- Created time

---

# 8. Job Discovery Architecture

Job sources should use a provider abstraction.

```text
Job Provider
     │
     ├── fetch()
     │
     ├── normalize()
     │
     ├── validate()
     │
     └── identify_duplicate()
```

Pipeline:

```text
Job Sources
    ↓
Fetch
    ↓
Normalize
    ↓
Validate
    ↓
Duplicate Detection
    ↓
Database
    ↓
Job Analyzer
    ↓
Match Engine
    ↓
User Recommendations
```

---

# 9. Job Matching

Use a hybrid approach.

## Stage 1 — Deterministic Matching

Evaluate:

```text
Skills
Experience
Role
Location
Employment Type
Salary
```

Example configurable weighting:

```text
Skills          40%
Experience      20%
Role            15%
Location        15%
Other           10%
```

These weights should remain configurable.

## Stage 2 — AI Analysis

AI evaluates:

- Semantic relevance
- Transferable skills
- Career alignment
- Missing requirements
- Potential concerns
- Recommendation context

Example:

```text
Candidate Profile
       +
Job Description
       ↓
Deterministic Matcher
       ↓
AI Analyzer
       ↓
Match Score
       +
Matched Skills
       +
Missing Skills
       +
Explanation
```

---

# 10. LinkedIn Content Architecture

```text
User Profile
     ↓
Topic Engine
     ↓
Previous Content
     ↓
Context Builder
     ↓
AI Writer
     ↓
Quality Checker
     ↓
Humanization
     ↓
Draft
     ↓
USER APPROVAL
     ↓
PUBLISH
```

The AI must not invent:

- Employment history
- Projects
- Certifications
- Technologies
- Metrics
- Job titles
- Achievements

All generated content should be grounded in verified user information.

---

# 11. Content Quality Pipeline

```text
Generate
   ↓
Fact Check
   ↓
Duplicate Check
   ↓
Tone Check
   ↓
Formatting Check
   ↓
Humanization
   ↓
Draft
```

Content statuses:

```text
DRAFT
REVIEW
APPROVED
SCHEDULED
PUBLISHED
ARCHIVED
```

---

# 12. Profile Monitoring

Profile monitoring uses snapshots.

```text
Current Profile
      ↓
Snapshot
      ↓
Previous Snapshot
      ↓
Diff Engine
      ↓
Detected Changes
      ↓
AI Analysis
      ↓
Recommendation
```

Track:

```text
Headline
About
Skills
Experience
Projects
Education
GitHub
Profile Completeness
```

---

# 13. GitHub Integration

```text
GitHub OAuth/API
       ↓
Repository Sync
       ↓
Activity Sync
       ↓
Technology Detection
       ↓
Significant Activity Detection
       ↓
Career Insight
       ↓
LinkedIn Content Suggestion
```

Example:

```text
New Repository
      ↓
Django + PostgreSQL + Redis
      ↓
Significant Project
      ↓
AI detects professional relevance
      ↓
LinkedIn post suggestion
```

---

# 14. Application State Machine

```text
NEW
 ↓
REVIEWED
 ↓
SAVED
 ↓
APPLIED
 ↓
INTERVIEW
 ↓
OFFER
```

Alternative:

```text
APPLIED
   ↓
REJECTED
```

Additional internal statuses may be added later.

---

# 15. Subscription Architecture

```text
User
  ↓
Subscription
  ↓
Plan
  ↓
Features + Limits + AI Credits
```

Example:

```text
FREE
 ↓
PRO
 ↓
PREMIUM
 ↓
TEAM
```

The application should check feature access centrally.

```text
Feature Request
      ↓
Subscription Service
      ↓
Plan Check
      ↓
Credit Check
      ↓
Allow / Deny
```

---

# 16. Billing Architecture

```text
User
  ↓
Select Plan
  ↓
Payment Provider
  ↓
Payment Success
  ↓
Webhook
  ↓
Billing Service
  ↓
Subscription Update
  ↓
Feature Access
```

Webhook processing must be idempotent.

---

# 17. AI Credit Flow

```text
AI Request
    ↓
Authentication
    ↓
Tenant Resolution
    ↓
Credit Check
    ↓
Execute AI Task
    ↓
Consume Credits
    ↓
Save AI Usage
    ↓
Return Result
```

AI usage should store:

```text
Tenant
User
Agent
Provider
Model
Input Tokens
Output Tokens
Credits
Latency
Timestamp
```

---

# 18. Celery Architecture

```text
                    REDIS
                      │
             ┌────────┴────────┐
             │                 │
             ▼                 ▼
        Celery Worker      Celery Beat
             │                 │
             ▼                 ▼
       Background Jobs     Scheduled Jobs
```

Suggested schedules:

```text
Job Discovery              Every 2 hours
GitHub Sync                Every 6 hours
Profile Monitoring         Daily
LinkedIn Draft             Daily
Daily Career Report        Daily
Weekly Analytics           Weekly
```

---

# 19. Notification System

Notification channels:

```text
Email
Telegram
In-App
```

Events:

```text
High Match Job
AI LinkedIn Draft
Application Reminder
Interview Reminder
Profile Issue
Subscription Event
Low AI Credits
GitHub Activity
```

Architecture:

```text
Application Event
       ↓
Notification Service
       ↓
Channel Selection
       ↓
Email / Telegram / In-App
```

---

# 20. API Architecture

Use layered architecture:

```text
HTTP Request
     ↓
Authentication
     ↓
Tenant Resolution
     ↓
Permission
     ↓
Serializer
     ↓
ViewSet
     ↓
Service
     ↓
ORM
     ↓
PostgreSQL
```

Views should remain thin.

Business logic belongs in service/domain layers.

---

# 21. Database Design

Primary database:

```text
PostgreSQL
```

Core entities:

```text
User
Tenant
UserProfile

Job
JobSkill
JobSource
JobApplication

LinkedInPost
PostTopic
PostPerformance

GitHubRepository
GitHubActivity

Agent
AgentTask
AgentExecution

AIUsage
AICreditTransaction

Plan
Subscription
Payment

Notification

ProfileSnapshot
CareerInsight
```

---

# 22. Database Indexing

Recommended indexes:

```text
tenant_id

tenant_id + status

tenant_id + created_at

tenant_id + match_score

Job:
title
company
location
published_at

Application:
status
applied_at

Post:
status
scheduled_at
```

Avoid excessive indexes because every additional index adds write overhead.

---

# 23. Redis

Redis is used for:

```text
Celery Broker
Caching
Rate Limiting
Temporary State
Agent Coordination
```

Cache keys should be tenant-aware.

Example:

```text
tenant:{tenant_id}:jobs:high-match
```

Never create cache keys that can accidentally mix tenant data.

---

# 24. Security Architecture

Implement:

```text
JWT Authentication
Tenant Isolation
Object-level Permissions
API Throttling
HTTPS
CSRF Protection
Input Validation
Secret Management
Webhook Validation
AI Output Validation
Audit Logging
```

Secrets belong in environment variables or a secure secret manager.

---

# 25. Human-in-the-Loop

The system should distinguish between AI assistance and external actions.

```text
AI
 ↓
Analyze
 ↓
Recommend
 ↓
Draft
 ↓
Notify
```

Then:

```text
USER
 ↓
Review
 ↓
Approve
 ↓
External Action
```

Sensitive actions include:

```text
Apply to Job
Publish LinkedIn Post
Send Recruiter Message
Modify Profile
```

---

# 26. Observability

Monitor:

```text
API Latency
Database Queries
Celery Tasks
AI Latency
AI Token Usage
AI Credit Consumption
Error Rates
External API Failures
Authentication Failures
```

Recommended future stack:

```text
Structured Logging
Sentry
Prometheus
Grafana
CloudWatch
```

---

# 27. Scalability

Initial architecture:

```text
One Django Application
       +
PostgreSQL
       +
Redis
       +
Celery
```

As usage grows:

```text
Load Balancer
      ↓
Multiple Django Instances
      ↓
Managed PostgreSQL
      +
Redis Cluster
      +
Multiple Celery Workers
      +
Dedicated AI Workers
```

---

# 28. Deployment

Production architecture:

```text
Internet
   ↓
AWS Load Balancer / Nginx
   ↓
Django / Next.js
   ↓
PostgreSQL
   +
Redis
   +
Celery Workers
```

Docker should be used for reproducible deployments.

---

# 29. Recommended Backend Apps

```text
accounts
tenants
profiles
jobs
applications
content
github
agents
ai
subscriptions
billing
notifications
analytics
```

Each app should have a focused responsibility.

---

# 30. Repository Structure

```text
linkedin-career-pilot-ai/
│
├── backend/
│   ├── core/
│   ├── apps/
│   ├── tests/
│   └── manage.py
│
├── frontend/
│
├── docker/
│
├── docs/
│   ├── README.md
│   ├── DESIGN.md
│   ├── FRONTEND.md
│   ├── API.md
│   └── BRAND.md
│
├── docker-compose.yml
└── .env.example
```

---

# 31. MVP Architecture

The first production-capable MVP should focus on:

```text
Authentication
      ↓
Profile
      ↓
Job Discovery
      ↓
Job Matching
      ↓
AI Job Analysis
      ↓
Application Tracking
      ↓
LinkedIn Content Generation
```

Then add:

```text
GitHub
Subscriptions
Notifications
Analytics
Advanced Agents
```

---

# 32. Product Principle

> **AI does the research, analysis, and preparation. The user stays in control.**

---

# 33. Long-Term Vision

```text
DISCOVER
   ↓
ANALYZE
   ↓
IMPROVE
   ↓
CREATE
   ↓
APPLY
   ↓
PREPARE
   ↓
INTERVIEW
   ↓
TRACK
   ↓
LEARN
   ↓
GROW
```

LinkedInCareerPilot AI should eventually become a unified professional career intelligence platform.
