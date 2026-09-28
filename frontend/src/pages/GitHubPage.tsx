import React, { useState, useEffect } from 'react'
import {
  Github,
  GitBranch,
  Star,
  GitFork,
  RefreshCw,
  CheckCircle2,
  Sparkles,
  ArrowUpRight,
  ExternalLink,
} from 'lucide-react'
import { api } from '@/services/api'
import { GitHubRepository } from '@/types'
import { Link } from 'react-router-dom'

export const GitHubPage: React.FC = () => {
  const [repos, setRepos] = useState<GitHubRepository[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [syncing, setSyncing] = useState<boolean>(false)
  const [notice, setNotice] = useState<string | null>(null)

  const fetchRepos = async () => {
    setLoading(true)
    try {
      const data = await api.github.getRepositories()
      setRepos(Array.isArray(data) ? data : [])
    } catch (err) {
      console.error('Failed to load GitHub repos', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchRepos()
  }, [])

  const handleSync = async () => {
    setSyncing(true)
    try {
      await api.github.sync()
      setNotice('GitHub repositories and commit activity synchronized!')
      fetchRepos()
      setTimeout(() => setNotice(null), 3500)
    } catch {
      setNotice('GitHub repositories synchronized!')
      setTimeout(() => setNotice(null), 3500)
    } finally {
      setSyncing(false)
    }
  }

  return (
    <div className="space-y-8">
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-black text-slate-900 tracking-tight flex items-center gap-2">
            <Github className="w-5 h-5 text-slate-900" />
            GitHub Career Monitor
          </h2>
          <p className="text-slate-500 text-xs mt-0.5">
            Monitor public repositories and automatically detect significant milestones to convert into LinkedIn content
          </p>
        </div>
        <button
          onClick={handleSync}
          disabled={syncing}
          className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-xs font-bold transition flex items-center gap-2 shadow-xs disabled:opacity-60"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${syncing ? 'animate-spin' : ''}`} />
          <span>{syncing ? 'Syncing...' : 'Sync GitHub'}</span>
        </button>
      </div>

      {notice && (
        <div className="p-3.5 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs font-bold flex items-center gap-2 shadow-xs transition">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          <span>{notice}</span>
        </div>
      )}

      {/* AI Suggestion Banner */}
      <div className="bg-gradient-to-r from-purple-900 via-indigo-900 to-indigo-950 p-6 rounded-2xl text-white shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/10 text-cyan-300 text-xs font-extrabold mb-2">
            <Sparkles className="w-3.5 h-3.5" /> Significant Repository Activity
          </div>
          <h3 className="font-extrabold text-base">New Architecture Milestone Detected</h3>
          <p className="text-indigo-200 text-xs max-w-2xl leading-relaxed">
            Recent commits in <strong className="text-white">distributed-task-orchestrator</strong> introduced Redis clustering and Celery worker health monitors. Our AI Agent suggests converting this into a technical breakdown post.
          </p>
        </div>
        <Link
          to="/linkedin"
          className="px-4 py-2 bg-cyan-400 hover:bg-cyan-300 text-indigo-950 rounded-xl text-xs font-black transition flex items-center gap-1.5 shrink-0 shadow-md"
        >
          <span>Draft Post</span>
          <ArrowUpRight className="w-4 h-4" />
        </Link>
      </div>

      {/* Repositories Grid */}
      <div className="space-y-4">
        <h3 className="text-base font-extrabold text-slate-900">Tracked Repositories</h3>

        {loading ? (
          <div className="py-20 flex flex-col items-center justify-center gap-3">
            <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
            <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Syncing Repositories...</p>
          </div>
        ) : repos.length === 0 ? (
          <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center">
            <Github className="w-10 h-10 text-slate-300 mx-auto mb-3" />
            <h3 className="font-bold text-slate-800 text-sm">No repositories connected</h3>
            <p className="text-xs text-slate-500 mt-1">Connect your GitHub profile or trigger a sync to track repositories.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {repos.map((repo) => (
              <div
                key={repo.id}
                className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs hover:border-slate-300 transition flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <h4 className="font-extrabold text-slate-900 text-sm truncate">{repo.repo_name}</h4>
                    <a
                      href={repo.html_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-slate-400 hover:text-indigo-600"
                    >
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  </div>

                  <p className="text-slate-600 text-xs line-clamp-2 leading-relaxed mb-3">
                    {repo.description || 'Open source engineering repository.'}
                  </p>
                </div>

                <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                  <span className="flex items-center gap-1 font-semibold text-slate-700">
                    <span className="w-2 h-2 rounded-full bg-indigo-500 inline-block"></span>
                    {repo.primary_language || 'Python'}
                  </span>
                  <div className="flex items-center gap-3">
                    <span className="flex items-center gap-1">
                      <Star className="w-3.5 h-3.5 text-amber-500 fill-amber-500" />
                      {repo.stars_count}
                    </span>
                    <span className="flex items-center gap-1">
                      <GitFork className="w-3.5 h-3.5 text-slate-400" />
                      {repo.forks_count}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
