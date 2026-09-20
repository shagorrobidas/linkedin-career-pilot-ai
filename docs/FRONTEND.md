# LinkedInCareerPilot AI — Frontend Design

> **Frontend architecture, UI system, components, and design guidelines**

---

# 1. Overview

The LinkedInCareerPilot AI frontend is a modern SaaS dashboard focused on:

```text
Career Information
        ↓
Recommended Actions
        ↓
AI Insights
        ↓
Career Analytics
        ↓
User Decisions
```

Recommended stack:

```text
Next.js
React
TypeScript
Tailwind CSS
shadcn/ui
Lucide Icons
TanStack Query
Zustand
React Hook Form
Zod
Recharts
```

Optional:

```text
Framer Motion
Sonner
date-fns
```

---

# 2. Frontend Architecture

```text
                         LINKEDINCAREERPILOT AI
                                  │
                                  ▼
                            NEXT.JS APP
                                  │
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
          ▼                       ▼                       ▼
        Pages                Components              Features
          │                       │                       │
          └───────────────────────┼───────────────────────┘
                                  ▼
                               Hooks
                                  │
                 ┌────────────────┴────────────────┐
                 │                                 │
                 ▼                                 ▼
          TanStack Query                       Zustand
          Server State                         UI State
                 │                                 │
                 └────────────────┬────────────────┘
                                  ▼
                           API SERVICE LAYER
                                  │
                                  ▼
                         DJANGO REST API
                                  │
                                  ▼
                     POSTGRESQL + REDIS
```

---

# 3. Recommended Stack

## Framework

```text
Next.js
```

## Language

```text
TypeScript
```

## UI

```text
Tailwind CSS
shadcn/ui
```

## Icons

```text
Lucide React
```

## Server State

```text
TanStack Query
```

## Client State

```text
Zustand
```

## Forms

```text
React Hook Form
Zod
```

## Charts

```text
Recharts
```

---

# 4. Folder Structure

```text
frontend/
│
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   ├── register/
│   │   └── forgot-password/
│   │
│   ├── (dashboard)/
│   │   ├── dashboard/
│   │   ├── jobs/
│   │   ├── applications/
│   │   ├── linkedin/
│   │   ├── profile/
│   │   ├── github/
│   │   ├── agents/
│   │   ├── analytics/
│   │   ├── billing/
│   │   └── settings/
│   │
│   ├── pricing/
│   ├── landing/
│   ├── layout.tsx
│   └── page.tsx
│
├── components/
│   ├── ui/
│   ├── layout/
│   ├── navigation/
│   ├── dashboard/
│   ├── jobs/
│   ├── applications/
│   ├── linkedin/
│   ├── profile/
│   ├── github/
│   ├── agents/
│   └── analytics/
│
├── features/
│   ├── auth/
│   ├── jobs/
│   ├── applications/
│   ├── linkedin/
│   ├── profile/
│   ├── github/
│   ├── agents/
│   ├── analytics/
│   └── billing/
│
├── hooks/
│
├── services/
│   ├── api.ts
│   ├── auth.ts
│   ├── jobs.ts
│   ├── applications.ts
│   ├── content.ts
│   ├── profile.ts
│   ├── github.ts
│   ├── agents.ts
│   └── billing.ts
│
├── store/
│   ├── auth-store.ts
│   ├── ui-store.ts
│   └── notification-store.ts
│
├── lib/
│   ├── utils.ts
│   ├── constants.ts
│   └── validators.ts
│
├── types/
├── config/
└── public/
```

---

# 5. Brand Colors

## Primary

```text
Primary       #4F46E5
Primary Dark  #3730A3
Secondary     #7C3AED
Accent        #06B6D4
Accent Soft   #CFFAFE
```

## Semantic

```text
Success       #16A34A
Success Soft  #DCFCE7

Warning       #F59E0B
Warning Soft  #FEF3C7

Danger        #DC2626
Danger Soft   #FEE2E2

Info          #0284C7
```

## Neutral

```text
Background      #F8FAFC
Surface         #FFFFFF
Surface Second  #F1F5F9

Text Primary    #0F172A
Text Secondary  #475569
Text Muted      #64748B
Text Disabled   #94A3B8

Border          #E2E8F0
Border Strong   #CBD5E1
```

---

# 6. Dark Mode

```text
Background      #020617
Surface         #0F172A
Surface Second  #1E293B

Text Primary    #F8FAFC
Text Secondary  #CBD5E1
Text Muted      #94A3B8

Border          #334155
```

---

# 7. Brand Gradient

Use the gradient selectively.

```text
#4F46E5
   ↓
#7C3AED
   ↓
#06B6D4
```

Recommended for:

- Hero backgrounds
- AI indicators
- Premium highlights
- Brand graphics
- Empty-state illustrations

Avoid using gradients on every component.

---

# 8. Typography

Recommended:

```text
Inter
```

Alternative:

```text
Plus Jakarta Sans
```

Code:

```text
JetBrains Mono
```

---

# 9. Typography Scale

```text
Display     48 / 56
H1          36 / 44
H2          30 / 38
H3          24 / 32
H4          20 / 28

Body Large  18 / 28
Body        16 / 24
Small       14 / 20
Caption     12 / 18
```

Font weights:

```text
Regular     400
Medium      500
Semibold    600
Bold        700
```

---

# 10. Buttons

Recommended:

```text
Height: 40–44px
Radius: 8–10px
Weight: 500–600
Padding: 12–18px
Transition: 150–200ms
```

## Primary

```text
Background: #4F46E5
Text: White

Hover:
#3730A3
```

Used for:

```text
Get Started
Generate Post
Analyze Job
Save Job
Upgrade Plan
```

## Secondary

```text
Background: #EEF2FF
Text: #3730A3
```

## Outline

```text
Background: Transparent
Border: #CBD5E1
Text: #0F172A
```

## Success

```text
Background: #16A34A
Text: White
```

## Danger

```text
Background: #DC2626
Text: White
```

## Ghost

```text
Background: Transparent
Text: #475569
```

---

# 11. Button States

Every interactive button should support:

```text
Default
Hover
Active
Focus
Disabled
Loading
```

Loading example:

```text
[ Spinner  Generating... ]
```

---

# 12. Cards

Default:

```text
Background: #FFFFFF
Border: 1px solid #E2E8F0
Radius: 12px
Padding: 20–24px
Shadow: Minimal
```

Cards should prioritize readability over excessive visual effects.

---

# 13. Application Layout

Desktop:

```text
┌─────────────────────────────────────────────────────────────┐
│                         TOP BAR                              │
├───────────────┬─────────────────────────────────────────────┤
│               │                                             │
│   SIDEBAR     │                  MAIN CONTENT               │
│               │                                             │
│ Dashboard     │                                             │
│ Jobs          │                                             │
│ Applications  │                                             │
│ LinkedIn      │                                             │
│ Profile       │                                             │
│ GitHub        │                                             │
│ AI Agents     │                                             │
│ Analytics     │                                             │
│ Billing       │                                             │
│ Settings      │                                             │
│               │                                             │
└───────────────┴─────────────────────────────────────────────┘
```

---

# 14. Sidebar

Navigation:

```text
Dashboard
Jobs
Applications
LinkedIn
Profile
GitHub
AI Agents
Analytics
Billing
Settings
```

Active state:

```text
Background: #EEF2FF
Text: #4F46E5
```

Sidebar should support:

```text
Expanded
Collapsed
Mobile Drawer
```

---

# 15. Top Bar

Include:

```text
Logo
Global Search
Notifications
AI Credits
Help
Profile Menu
```

Example:

```text
[ LinkedInCareerPilot AI ]

Search...

                    🔔   ⚡ 82/100   👤
```

---

# 16. Dashboard

Primary KPI cards:

```text
Jobs Discovered
High Match Jobs
Applications
Interviews
Offers
LinkedIn Posts
```

Example:

```text
┌──────────────┐
│ Jobs         │
│              │
│ 128          │
│ +18 this week│
└──────────────┘
```

---

# 17. Dashboard Sections

Recommended order:

```text
1. Career Overview
2. Recommended Actions
3. High-Match Jobs
4. Application Pipeline
5. AI Insights
6. LinkedIn Content
7. GitHub Activity
8. Career Analytics
```

The most important information should appear first.

---

# 18. Job Card

Each job card should display:

```text
Company
Job Title
Location
Employment Type
Match Score
Matched Skills
Missing Skills
Published Date
```

Actions:

```text
View Job
Save
Analyze
Track Application
```

Example:

```text
Backend Engineer

Example Technologies

📍 Remote
💼 Full-time

94% Match

✓ Python
✓ Django
✓ PostgreSQL
✓ Redis

Missing:
Kubernetes

[ View Job ] [ Save ]
```

---

# 19. Match Score

Suggested categories:

```text
90–100    High
70–89     Medium
0–69      Low
```

Use semantic colors:

```text
High      Success
Medium    Warning
Low       Danger
```

The UI should explain why a match score was produced instead of showing only a number.

---

# 20. Application Tracker

Table:

```text
Company
Position
Match
Location
Status
Date
Action
```

Example statuses:

```text
NEW
REVIEWED
SAVED
APPLIED
INTERVIEW
OFFER
REJECTED
```

Mobile should transform tables into cards.

---

# 21. LinkedIn Content Page

Main layout:

```text
┌──────────────────────────────────────────────┐
│ Generate LinkedIn Post                       │
├──────────────────────────────────────────────┤
│ Topic                                        │
│ [ Django Performance                         │
│                                              │
│ Tone                                         │
│ [ Professional ▼ ]                           │
│                                              │
│ Context                                      │
│ [ Project / Learning / Career ▼ ]            │
│                                              │
│ [ Generate ]                                 │
└──────────────────────────────────────────────┘
```

Generated content:

```text
┌──────────────────────────────────────────────┐
│ AI Generated Post                            │
│                                              │
│ [Generated LinkedIn content]                 │
│                                              │
│ [Edit] [Regenerate] [Approve]                │
└──────────────────────────────────────────────┘
```

---

# 22. Profile Health

Display:

```text
Headline
About
Skills
Experience
Projects
GitHub
```

Example:

```text
PROFILE HEALTH

Overall
87%

Headline       92%
About          76%
Skills         94%
Projects       90%
GitHub         88%
```

Show actionable recommendations below the score.

---

# 23. GitHub Dashboard

Display:

```text
Repositories
Languages
Recent Activity
Projects
Technology Usage
AI Career Insights
```

Example:

```text
Recent Activity

StudyBuddy
Django Channels
3 commits
2 days ago

AI Insight:
This project demonstrates real-time
backend architecture skills.
```

---

# 24. AI Agent Dashboard

Agent cards:

```text
Job Hunter
Job Analyzer
LinkedIn Writer
Profile Guardian
GitHub Monitor
Career Analyst
Interview Agent
```

Each card should show:

```text
Agent Name
Status
Last Run
Current Task
Credits Used
Action
```

Statuses:

```text
Running
Completed
Waiting
Failed
Paused
```

---

# 25. AI Credits

Display prominently but unobtrusively.

Example:

```text
⚡ 82 / 100 AI Credits
```

Clicking opens:

```text
Credits Used
Credits Remaining
Usage History
Plan Limit
Upgrade
```

---

# 26. Pricing Page

Plans:

```text
Free
Pro
Premium
Team
```

Each plan should show:

```text
Price
AI Credits
Job Matching
LinkedIn Content
GitHub Monitoring
Analytics
Career Tools
```

Primary CTA:

```text
Start Free
Upgrade
```

---

# 27. Landing Page

Recommended structure:

```text
Navbar
   ↓
Hero
   ↓
Social Proof
   ↓
Core Features
   ↓
How It Works
   ↓
AI Agents
   ↓
Dashboard Preview
   ↓
Career Workflow
   ↓
Pricing
   ↓
FAQ
   ↓
CTA
   ↓
Footer
```

---

# 28. Hero Section

Headline:

```text
Build Your Career.
Let AI Handle the Busywork.
```

Supporting text:

```text
LinkedInCareerPilot AI helps you discover opportunities,
create professional content, track applications, monitor
your career activity, and make smarter career decisions.
```

CTA:

```text
Get Started Free
Explore Features
```

---

# 29. How It Works

```text
01
Connect Your Profile

        ↓

02
AI Understands Your Career

        ↓

03
Discover Opportunities

        ↓

04
Create & Improve Content

        ↓

05
Track Applications

        ↓

06
Grow Your Career
```

---

# 30. Responsive Design

## Desktop

```text
Sidebar
+
Top Navigation
+
Main Content
```

## Tablet

```text
Collapsed Sidebar
+
Top Navigation
+
Main Content
```

## Mobile

```text
Top Navigation
+
Content
+
Bottom Navigation
```

Mobile bottom navigation:

```text
Home
Jobs
Applications
AI
Profile
```

---

# 31. Breakpoints

Tailwind defaults:

```text
sm   640px
md   768px
lg   1024px
xl   1280px
2xl  1536px
```

---

# 32. Spacing

Use a 4px base unit.

```text
4
8
12
16
20
24
32
40
48
64
80
```

Avoid arbitrary spacing unless necessary.

---

# 33. Border Radius

```text
Small       6px
Default     8px
Card        12px
Large       16px
Pill        9999px
```

---

# 34. Icons

Use:

```text
Lucide React
```

Suggested icons:

```text
Dashboard       LayoutDashboard
Jobs            Briefcase
Applications    ClipboardCheck
LinkedIn        Linkedin
Profile         UserRound
GitHub          Github
AI              Sparkles
Analytics       ChartNoAxesCombined
Billing         CreditCard
Settings        Settings
Notifications   Bell
Search          Search
```

---

# 35. Forms

Input:

```text
Height: 44px
Radius: 8px
Border: #CBD5E1
```

Focus:

```text
Border: #4F46E5
Ring: #EEF2FF
```

Forms should include:

```text
Label
Input
Helper Text
Validation
Error Message
```

---

# 36. Tables

Desktop:

```text
Company
Position
Match
Location
Status
Date
Action
```

Mobile:

```text
Table
   ↓
Responsive Card List
```

Avoid horizontal scrolling where possible.

---

# 37. Empty States

Every major page should have an intentional empty state.

Example:

```text
No saved jobs yet.

Start discovering relevant opportunities
and save jobs you want to track.

[ Find Jobs ]
```

---

# 38. Loading States

Use skeleton loaders for:

```text
Dashboard
Job Cards
Profile
Analytics
Application Table
GitHub Activity
```

Avoid blank screens during loading.

---

# 39. Toast Notifications

Use toast messages for:

```text
Job Saved
Application Updated
Post Generated
Post Approved
Profile Updated
GitHub Connected
Subscription Updated
```

Recommended library:

```text
Sonner
```

---

# 40. State Management

Use **TanStack Query** for server state:

```text
Jobs
Applications
Profile
GitHub
Analytics
Agents
Billing
```

Use **Zustand** for client/UI state:

```text
Sidebar
Theme
Modal
Notifications
Temporary UI preferences
```

Avoid putting server data unnecessarily into Zustand.

---

# 41. API Service Layer

Example:

```text
services/
├── api.ts
├── auth.ts
├── jobs.ts
├── applications.ts
├── content.ts
├── profile.ts
├── github.ts
├── agents.ts
└── billing.ts
```

Each service should communicate with Django REST APIs.

---

# 42. Authentication Flow

```text
Login
  ↓
Django Authentication
  ↓
JWT Access Token
  +
Refresh Token
  ↓
Frontend Session
  ↓
Authenticated API Requests
```

Support future OAuth providers where appropriate.

---

# 43. Error Handling

Handle:

```text
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Validation Error
429 Rate Limited
500 Server Error
```

Example:

```text
Something went wrong.

We couldn't analyze this job right now.

[ Try Again ]
```

Never expose internal stack traces to users.

---

# 44. Accessibility

The frontend should support:

```text
Keyboard Navigation
Screen Readers
Visible Focus States
Semantic HTML
Accessible Labels
Sufficient Contrast
Reduced Motion
```

Interactive elements must have accessible names.

---

# 45. Performance

Optimize:

```text
Image Loading
Code Splitting
Lazy Loading
API Requests
Caching
Bundle Size
Rendering
```

Use:

```text
Next.js Image
Dynamic Imports
TanStack Query Cache
Server Components where appropriate
```

---

# 46. SEO

Public pages should have:

```text
Title
Meta Description
Open Graph
Twitter/X Metadata
Canonical URL
Structured Data where useful
```

Dashboard/private pages do not need public SEO optimization.

---

# 47. Frontend Security

Never expose:

```text
OPENAI_API_KEY
GEMINI_API_KEY
DATABASE_URL
JWT signing secrets
Payment secrets
GitHub private tokens
```

Sensitive operations must go through the backend.

Frontend environment variables should only contain values safe for browser exposure.

---

# 48. Component Architecture

Prefer reusable components:

```text
Button
Card
Modal
Input
Select
Badge
Table
Tabs
Dropdown
Tooltip
Skeleton
Toast
Dialog
```

Feature-specific components:

```text
JobCard
MatchScore
ApplicationStatus
PostEditor
ProfileHealth
AgentCard
GithubActivity
CareerInsight
```

---

# 49. Animation Guidelines

Use subtle animations only.

Good uses:

```text
Page transitions
Card hover
Loading
Modal
Dropdown
AI generation
Progress indicators
```

Avoid excessive animations that distract from career information.

---

# 50. Design Priority

The UI should prioritize information in this order:

```text
1. Career Information
2. Recommended Actions
3. AI Insights
4. Primary Metrics
5. Secondary Information
6. Technical Details
```

---

# 51. Visual Direction

The final visual direction is:

```text
Modern SaaS
      +
AI Workspace
      +
Career Dashboard
      +
Developer Tool
```

Visual identity:

```text
Indigo
+
Purple
+
Cyan
+
White
+
Slate
```

Typography:

```text
Inter
+
JetBrains Mono
```

Icons:

```text
Lucide
```

---

# 52. Design Principles

### 1. Simple

Users should understand the interface immediately.

### 2. Actionable

Every insight should lead to a possible action.

### 3. Trustworthy

AI-generated information should be clearly identified.

### 4. Human-Controlled

Important external actions require user approval.

### 5. Consistent

Colors, spacing, typography, buttons, cards, and states should behave consistently.

### 6. Career-Focused

The dashboard should always prioritize meaningful career information.

---

# 53. Final Frontend Architecture

```text
                         LINKEDINCAREERPILOT AI
                                  │
                                  ▼
                             NEXT.JS APP
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             ▼                    ▼                    ▼
           Pages             Components           Features
             │                    │                    │
             └────────────────────┼────────────────────┘
                                  ▼
                                Hooks
                                  │
                  ┌───────────────┴───────────────┐
                  │                               │
                  ▼                               ▼
           TanStack Query                       Zustand
           Server State                         UI State
                  │                               │
                  └───────────────┬───────────────┘
                                  ▼
                           API SERVICE LAYER
                                  │
                                  ▼
                         DJANGO REST API
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             ▼                    ▼                    ▼
            Jobs               Content              Profile
             │                    │                    │
             ▼                    ▼                    ▼
       Applications          AI Agents             GitHub
                                  │
                                  ▼
                        PostgreSQL + Redis
```

---

# 54. Product Experience Goal

The frontend should make the user's daily workflow feel like:

```text
OPEN DASHBOARD
      ↓
SEE WHAT MATTERS
      ↓
REVIEW AI INSIGHTS
      ↓
DISCOVER OPPORTUNITIES
      ↓
CREATE / IMPROVE CONTENT
      ↓
TRACK APPLICATIONS
      ↓
TAKE ACTION
      ↓
MEASURE PROGRESS
```

> **LinkedInCareerPilot AI — Simple enough to understand. Powerful enough to manage your professional growth.**
