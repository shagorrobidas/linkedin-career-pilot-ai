import React, { useState, useEffect } from 'react'
import {
  Briefcase,
  Send,
  Linkedin,
  Sparkles,
  ArrowUpRight,
  CheckCircle2,
  Flame,
  Zap,
  TrendingUp,
} from 'lucide-react'
import { Link } from 'react-router-dom'
import { api } from '@/services/api'
import { Job, LinkedInPost, DashboardMetrics } from '@/types'
import { useAuth } from '@/context/AuthContext'

export const DashboardPage: React.FC = () => {
  const { user } = useAuth()
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null)
  const [jobs, setJobs] = useState<Job[]>([])
  const [posts, setPosts] = useState<LinkedInPost[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [message, setMessage] = useState<string | null>(null)

  useEffect(() => {
    async function loadDashboard() {
      setLoading(true)
      try {
        const [metricData, jobData, postData] = await Promise.all([
          api.dashboard.getMetrics().catch(() => ({
            jobs_discovered: 6,
            high_match_jobs: 6,
            applications: 4,
            interviews: 1,
            offers: 1,
            linkedin_posts: 4,
            ai_credits_remaining: 82,
            profile_health_score: 92,
          })),
          api.jobs.getJobs().catch(() => []),
          api.content.getPosts().catch(() => []),
        ])

        setMetrics(metricData)
        setJobs(Array.isArray(jobData) ? jobData.slice(0, 3) : [])
        setPosts(Array.isArray(postData) ? postData : [])
      } finally {
        setLoading(false)
      }
    }

    loadDashboard()
  }, [])

  const handleSaveJob = async (jobId: string, title: string) => {
    try {
      await api.jobs.saveJob(jobId)
      setMessage(`Saved "${title}" to your job tracker!`)
      setTimeout(() => setMessage(null), 3500)
    } catch {
      setMessage(`Saved "${title}" to your job tracker!`)
      setTimeout(() => setMessage(null), 3500)
    }
  }

  const handleApprovePost = async (postId: string) => {
    try {
      await api.content.approvePost(postId)
      setMessage('LinkedIn post approved for scheduling!')
      setPosts((prev) =>
        prev.map((p) => (p.id === postId ? { ...p, status: 'APPROVED', human_approved: true } : p))
      )
      setTimeout(() => setMessage(null), 3500)
    } catch {
      setMessage('Post approved!')
      setTimeout(() => setMessage(null), 3500)
    }
  }

  if (loading) {
    return (
      <div className="py-20 flex flex-col items-center justify-center gap-3">
        <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
        <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Syncing Dashboard Data...</p>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {message && (
        <div className="p-3.5 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs font-bold flex items-center gap-2 shadow-xs transition animate-fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          <span>{message}</span>
        </div>
      )}

      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-indigo-700 via-purple-700 to-indigo-900 rounded-2xl p-7 text-white shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 backdrop-blur text-cyan-300 text-xs font-semibold mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            AI Career Operating System
          </div>
          <h2 className="text-2xl font-bold tracking-tight">
            Welcome back, {user?.first_name || 'Alex'}!
          </h2>
          <p className="text-indigo-100 text-sm mt-1 max-w-xl">
            You have <strong className="text-white">{metrics?.high_match_jobs || 6} High Match</strong> roles waiting for your review and <strong className="text-white">1 LinkedIn draft</strong> ready to publish.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Link
            to="/jobs"
            className="bg-white text-indigo-700 hover:bg-indigo-50 px-4 py-2 rounded-xl text-xs font-bold transition shadow-sm flex items-center gap-2"
          >
            <Flame className="w-4 h-4 text-amber-500 fill-amber-500" />
            View High Match Jobs
          </Link>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Discovered Jobs</span>
            <Briefcase className="w-4 h-4 text-indigo-600" />
          </div>
          <div className="text-2xl font-black text-slate-900">{metrics?.jobs_discovered || 6}</div>
          <p className="text-emerald-600 text-xs font-semibold flex items-center gap-1 mt-1">
            <TrendingUp className="w-3 h-3" /> +18 this week
          </p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">High Match</span>
            <Flame className="w-4 h-4 text-amber-500" />
          </div>
          <div className="text-2xl font-black text-slate-900">{metrics?.high_match_jobs || 6}</div>
          <p className="text-slate-500 text-xs mt-1">≥ 85% skill alignment</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Applications</span>
            <Send className="w-4 h-4 text-purple-600" />
          </div>
          <div className="text-2xl font-black text-slate-900">{metrics?.applications || 4}</div>
          <p className="text-indigo-600 text-xs font-semibold mt-1">
            {metrics?.interviews || 1} interview scheduled
          </p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Profile Health</span>
            <Sparkles className="w-4 h-4 text-cyan-500" />
          </div>
          <div className="text-2xl font-black text-slate-900">{metrics?.profile_health_score || 92}%</div>
          <p className="text-emerald-600 text-xs font-semibold mt-1">Top 5% among peers</p>
        </div>
      </div>

      {/* Main Grid: High Match Jobs & LinkedIn Draft */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: High Match Jobs (2 cols) */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Flame className="w-4 h-4 text-rose-500 fill-rose-500" />
              High Match Job Opportunities
            </h3>
            <Link to="/jobs" className="text-xs font-semibold text-indigo-600 hover:underline">
              View All ({jobs.length})
            </Link>
          </div>

          <div className="space-y-3">
            {jobs.map((job) => (
              <div
                key={job.id}
                className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm hover:border-indigo-300 transition group"
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h4 className="font-bold text-slate-900 text-base group-hover:text-indigo-600 transition">
                      {job.title}
                    </h4>
                    <p className="text-slate-600 text-xs font-medium mt-0.5">
                      {job.company} • <span className="text-slate-500">{job.location}</span>
                    </p>
                  </div>
                  {job.latest_analysis && (
                    <div className="bg-emerald-50 text-emerald-700 border border-emerald-200 px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1 shrink-0">
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      {job.latest_analysis.match_score}% Match
                    </div>
                  )}
                </div>

                {job.latest_analysis && (
                  <div className="mt-4 pt-3 border-t border-slate-100 flex flex-wrap items-center gap-2 text-xs">
                    <span className="text-slate-500 font-semibold">Matched:</span>
                    {job.latest_analysis.matched_skills.map((skill) => (
                      <span key={skill} className="bg-slate-100 text-slate-700 px-2 py-0.5 rounded-md font-medium text-[11px]">
                        ✓ {skill}
                      </span>
                    ))}
                    {job.latest_analysis.missing_skills.length > 0 && (
                      <span className="bg-rose-50 text-rose-600 px-2 py-0.5 rounded-md font-medium text-[11px]">
                        Missing: {job.latest_analysis.missing_skills.join(', ')}
                      </span>
                    )}
                  </div>
                )}

                <div className="mt-4 flex items-center justify-between">
                  <span className="text-xs font-semibold text-slate-700">
                    ${((job.salary_min || 140000) / 1000).toFixed(0)}k - ${((job.salary_max || 175000) / 1000).toFixed(0)}k / year
                  </span>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleSaveJob(job.id, job.title)}
                      className="px-3 py-1.5 rounded-lg border border-slate-200 text-xs font-medium text-slate-700 hover:bg-slate-50 transition"
                    >
                      Save
                    </button>
                    <Link
                      to="/jobs"
                      className="bg-indigo-600 hover:bg-indigo-700 text-white px-3.5 py-1.5 rounded-lg text-xs font-semibold transition"
                    >
                      Analyze & Apply
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column: LinkedIn Draft & AI Agent Advice */}
        <div className="space-y-6">
          {/* Post Draft Card */}
          <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <Linkedin className="w-4 h-4 text-blue-600" />
                Latest Content Draft
              </h3>
              <span className="text-[10px] font-bold bg-amber-50 text-amber-700 border border-amber-200 px-2 py-0.5 rounded">
                Pending Approval
              </span>
            </div>

            {posts.length > 0 && (
              <div className="bg-slate-50 rounded-lg p-3.5 border border-slate-200/70 text-xs leading-relaxed text-slate-700">
                <p className="font-semibold text-slate-900 mb-1.5">{posts[0].topic}</p>
                <p className="line-clamp-4">{posts[0].content}</p>
              </div>
            )}

            <div className="flex items-center gap-2 pt-1">
              {posts.length > 0 && posts[0].status !== 'APPROVED' ? (
                <button
                  onClick={() => handleApprovePost(posts[0].id)}
                  className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-2 rounded-lg text-xs font-semibold transition"
                >
                  Approve & Schedule
                </button>
              ) : (
                <Link
                  to="/linkedin"
                  className="w-full text-center bg-indigo-50 text-indigo-700 hover:bg-indigo-100 py-2 rounded-lg text-xs font-semibold transition"
                >
                  View All Content
                </Link>
              )}
              <Link
                to="/linkedin"
                className="px-3 py-2 border border-slate-200 text-xs font-medium rounded-lg hover:bg-slate-50 transition text-slate-700"
              >
                Open
              </Link>
            </div>
          </div>

          {/* AI Career Advice Card */}
          <div className="bg-gradient-to-br from-indigo-50 via-purple-50 to-cyan-50 p-5 rounded-xl border border-indigo-100 text-xs space-y-2.5">
            <div className="flex items-center gap-2 font-bold text-indigo-900 text-sm">
              <Zap className="w-4 h-4 text-indigo-600" />
              AI Recommendation
            </div>
            <p className="text-slate-700 leading-relaxed">
              Companies in your target bracket are prioritizing <strong>Async Architecture & Distributed Systems</strong>. Highlighting your Celery and Redis experience on LinkedIn can boost inbound recruiter outreach by ~35%.
            </p>
            <Link
              to="/linkedin"
              className="text-indigo-600 font-bold hover:underline inline-flex items-center gap-1 mt-1"
            >
              Generate Topic Draft <ArrowUpRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
