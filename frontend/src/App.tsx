import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from '@/context/AuthContext'
import { ProtectedRoute } from '@/components/layout/ProtectedRoute'

import { LoginPage } from '@/pages/LoginPage'
import { RegisterPage } from '@/pages/RegisterPage'
import { DashboardPage } from '@/pages/DashboardPage'
import { JobsPage } from '@/pages/JobsPage'
import { ApplicationsPage } from '@/pages/ApplicationsPage'
import { LinkedInPage } from '@/pages/LinkedInPage'
import { ProfilePage } from '@/pages/ProfilePage'
import { GitHubPage } from '@/pages/GitHubPage'
import { AIAgentsPage } from '@/pages/AIAgentsPage'
import { AnalyticsPage } from '@/pages/AnalyticsPage'
import { BillingPage } from '@/pages/BillingPage'

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Public Authentication Routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Protected Application Routes */}
          <Route element={<ProtectedRoute />}>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/jobs" element={<JobsPage />} />
            <Route path="/applications" element={<ApplicationsPage />} />
            <Route path="/linkedin" element={<LinkedInPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/github" element={<GitHubPage />} />
            <Route path="/agents" element={<AIAgentsPage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
            <Route path="/billing" element={<BillingPage />} />
          </Route>

          {/* Catch-all redirect */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
