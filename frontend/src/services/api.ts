import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios'
import {
  AuthTokens,
  User,
  DashboardMetrics,
  Job,
  JobApplication,
  LinkedInPost,
  ProfileHealth,
  UserProfile,
  GitHubRepository,
  Agent,
  Plan,
  Subscription,
  NotificationItem,
  CareerInsightItem
} from '@/types'

// Resolve API base URL: environment variable or default fallback
const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1'

export const apiClient: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
})

// Request Interceptor: Inject JWT token into Authorization header
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error: AxiosError) => Promise.reject(error)
)

// Response Interceptor: Extract response data and handle auth expiration
apiClient.interceptors.response.use(
  (response) => {
    // If response contains DRF standard payload structure { success: true, data: ... }
    if (response.data && response.data.data !== undefined) {
      return response.data.data
    }
    return response.data
  },
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // If unauthorized on a protected resource, we can clear tokens
      // Avoid clearing if on login endpoint itself
      if (!error.config?.url?.includes('/auth/login')) {
        // Token expired or invalid
        console.warn('Session expired or unauthorized request.')
      }
    }
    return Promise.reject(error)
  }
)

export const api = {
  // Authentication
  auth: {
    login: (credentials: { email: string; password: string }): Promise<AuthTokens> =>
      apiClient.post('/auth/login/', credentials),
    register: (payload: { email: string; password: string; first_name?: string; last_name?: string }): Promise<AuthTokens> =>
      apiClient.post('/auth/register/', payload),
    me: (): Promise<User> =>
      apiClient.get('/auth/me/'),
  },

  // Dashboard Overview
  dashboard: {
    getMetrics: (): Promise<DashboardMetrics> =>
      apiClient.get('/dashboard/'),
  },

  // Jobs
  jobs: {
    getJobs: (params?: { work_mode?: string; search?: string }): Promise<Job[]> => {
      const q = new URLSearchParams()
      if (params?.work_mode && params.work_mode !== 'ALL') q.set('work_mode', params.work_mode)
      if (params?.search) q.set('search', params.search)
      const url = `/jobs/${q.toString() ? '?' + q.toString() : ''}`
      return apiClient.get(url)
    },
    getJob: (id: string): Promise<Job> =>
      apiClient.get(`/jobs/${id}/`),
    analyzeJob: (id: string): Promise<any> =>
      apiClient.post(`/jobs/${id}/analyze/`),
    saveJob: (id: string): Promise<{ success: boolean; message: string }> =>
      apiClient.post(`/jobs/${id}/save_job/`),
  },

  // Applications
  applications: {
    getApplications: (status?: string): Promise<JobApplication[]> => {
      const url = status && status !== 'ALL' ? `/applications/?status=${status}` : '/applications/'
      return apiClient.get(url)
    },
    updateStatus: (id: string, newStatus: string): Promise<JobApplication> =>
      apiClient.patch(`/applications/${id}/update_status/`, { status: newStatus }),
  },

  // LinkedIn Content
  content: {
    getPosts: (): Promise<LinkedInPost[]> =>
      apiClient.get('/content/'),
    generatePost: (topic: string, tone: string = 'PROFESSIONAL'): Promise<LinkedInPost> =>
      apiClient.post('/content/generate/', { topic, tone }),
    approvePost: (id: string): Promise<LinkedInPost> =>
      apiClient.post(`/content/${id}/approve/`),
    schedulePost: (id: string, scheduled_at: string): Promise<LinkedInPost> =>
      apiClient.post(`/content/${id}/schedule/`, { scheduled_at }),
  },

  // Profile & Health
  profile: {
    getProfile: (): Promise<UserProfile> =>
      apiClient.get('/profile/'),
    getHealth: (): Promise<ProfileHealth> =>
      apiClient.get('/profile/health/'),
    updateProfile: (data: Partial<UserProfile>): Promise<UserProfile> =>
      apiClient.patch('/profile/', data),
  },

  // GitHub Monitor
  github: {
    getRepositories: (): Promise<GitHubRepository[]> =>
      apiClient.get('/github/repositories/'),
    sync: (): Promise<{ success: boolean; message: string }> =>
      apiClient.post('/github/repositories/sync/'),
  },

  // AI Agents
  agents: {
    getAgents: (): Promise<Agent[]> =>
      apiClient.get('/agents/'),
    runAgent: (agentId: string, payload: any): Promise<any> =>
      apiClient.post(`/agents/${agentId}/run/`, payload),
    getCredits: (): Promise<{ credits_available: number; credits_total: number; used_this_month: number }> =>
      apiClient.get('/agents/credits/'),
  },

  // Subscriptions & Plans
  subscriptions: {
    getPlans: (): Promise<Plan[]> =>
      apiClient.get('/subscriptions/plans/'),
    getCurrent: (): Promise<Subscription> =>
      apiClient.get('/subscriptions/'),
    changePlan: (plan_type: string): Promise<{ success: boolean; message: string }> =>
      apiClient.post('/subscriptions/change_plan/', { plan_type }),
  },

  // Notifications
  notifications: {
    getNotifications: (): Promise<NotificationItem[]> =>
      apiClient.get('/notifications/'),
    markRead: (id: string): Promise<{ success: boolean; message: string }> =>
      apiClient.post(`/notifications/${id}/mark_read/`),
  },

  // Analytics
  analytics: {
    getSummary: (): Promise<any> =>
      apiClient.get('/analytics/summary/'),
    getInsights: (): Promise<CareerInsightItem[]> =>
      apiClient.get('/analytics/insights/'),
  },
}
