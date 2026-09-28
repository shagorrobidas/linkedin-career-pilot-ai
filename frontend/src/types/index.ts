export interface User {
  id: string
  email: string
  first_name: string
  last_name: string
  full_name?: string
  is_active: boolean
  created_at: string
  tenant?: {
    id: string
    name: string
    role: string
  }
}

export interface AuthTokens {
  access_token: string
  refresh_token: string
  user: User
}

export interface UserProfile {
  id: string
  headline: string
  about: string
  career_focus: string
  years_of_experience: number
  location: string
  remote_preference: string
  desired_salary_min?: number
  desired_salary_currency?: string
  resume_url?: string
  profile_completion: number
  skills: Array<{ id: string; name: string; years_of_experience: number; is_primary: boolean }>
  experiences: Array<{
    id: string
    title: string
    company: string
    location: string
    start_date: string
    end_date?: string
    is_current: boolean
    description: string
    skills_used: string[]
  }>
  educations: Array<{
    id: string
    institution: string
    degree: string
    field_of_study: string
    start_date?: string
    end_date?: string
  }>
}

export interface ProfileHealth {
  overall_health_score: number
  headline_score: number
  about_score: number
  skills_score: number
  projects_score: number
  github_score: number
  suggestions: string[]
}

export interface Job {
  id: string
  title: string
  company: string
  description: string
  location: string
  work_mode: 'REMOTE' | 'HYBRID' | 'ON_SITE' | string
  employment_type: string
  salary_min?: number
  salary_max?: number
  currency: string
  application_url?: string
  skills?: Array<{ id: string; name: string; required: boolean; importance: number }>
  latest_analysis?: {
    match_score: number
    matched_skills: string[]
    missing_skills: string[]
    experience_compatibility: string
    career_alignment: string
    recommendation: string
  }
}

export interface JobApplication {
  id: string
  job: string
  job_details?: Job
  status: 'NEW' | 'REVIEWED' | 'SAVED' | 'APPLIED' | 'INTERVIEW' | 'OFFER' | 'REJECTED' | 'ARCHIVED'
  applied_date?: string
  recruiter_name?: string
  recruiter_email?: string
  notes?: string
  created_at?: string
  updated_at?: string
}

export interface LinkedInPost {
  id: string
  topic: string
  content: string
  tone: 'PROFESSIONAL' | 'CASUAL' | 'THOUGHT_LEADERSHIP' | 'STORYTELLING' | 'EDUCATIONAL' | string
  status: 'DRAFT' | 'REVIEW' | 'APPROVED' | 'SCHEDULED' | 'PUBLISHED' | 'ARCHIVED'
  scheduled_at?: string
  published_at?: string
  ai_generated: boolean
  human_approved: boolean
  performance?: {
    impressions: number
    reactions: number
    comments: number
    shares: number
    profile_views_generated?: number
  }
}

export interface GitHubRepository {
  id: string
  repo_name: string
  full_name: string
  description: string
  html_url: string
  primary_language: string
  languages: Record<string, number>
  stars_count: number
  forks_count: number
  is_fork: boolean
  is_private: boolean
  activities?: Array<{
    id: string
    activity_type: string
    title: string
    description: string
    occurred_at: string
  }>
}

export interface Agent {
  id: string
  name: string
  slug: string
  description: string
  provider: string
  model_name: string
  credit_cost: number
  is_active: boolean
}

export interface DashboardMetrics {
  jobs_discovered: number
  high_match_jobs: number
  applications: number
  interviews: number
  offers: number
  linkedin_posts: number
  ai_credits_remaining: number
  profile_health_score: number
}

export interface Plan {
  id: string
  name: string
  plan_type: 'FREE' | 'PRO' | 'PREMIUM' | 'TEAM'
  price_monthly: number
  price_yearly: number
  ai_credits_monthly: number
  features: string[]
  is_active: boolean
}

export interface Subscription {
  id?: string
  plan: Plan
  status: string
  ai_credits_remaining: number
  current_period_end?: string
}

export interface NotificationItem {
  id: string
  title: string
  message: string
  notification_type: string
  is_read: boolean
  created_at: string
}

export interface CareerInsightItem {
  id?: string
  category: string
  title: string
  description: string
  actionable_step?: string
}
