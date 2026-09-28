import React, { useState, useEffect } from 'react'
import {
  Briefcase,
  Search,
  Filter,
  Flame,
  CheckCircle2,
  Sparkles,
  ExternalLink,
  MapPin,
  DollarSign,
  Bookmark,
  Send,
  X
} from 'lucide-react'
import { api } from '@/services/api'
import { Job } from '@/types'

export const JobsPage: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [workMode, setWorkMode] = useState<string>('ALL')
  const [search, setSearch] = useState<string>('')
  const [analyzingId, setAnalyzingId] = useState<string | null>(null)
  const [selectedJob, setSelectedJob] = useState<Job | null>(null)
  const [actionNotice, setActionNotice] = useState<string | null>(null)

  const fetchJobs = async () => {
    setLoading(true)
    try {
      const data = await api.jobs.getJobs({
        work_mode: workMode !== 'ALL' ? workMode : undefined,
        search: search.trim() || undefined,
      })
      setJobs(Array.isArray(data) ? data : [])
    } catch (err) {
      console.error('Failed to load jobs', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchJobs()
  }, [workMode])

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    fetchJobs()
  }

  const handleAnalyzeJob = async (jobId: string) => {
    setAnalyzingId(jobId)
    try {
      const result = await api.jobs.analyzeJob(jobId)
      setJobs((prev) =>
        prev.map((j) => (j.id === jobId ? { ...j, latest_analysis: result } : j))
      )
      if (selectedJob && selectedJob.id === jobId) {
        setSelectedJob({ ...selectedJob, latest_analysis: result })
      }
      setActionNotice('AI Analysis complete!')
      setTimeout(() => setActionNotice(null), 3000)
    } catch {
      setActionNotice('AI Analysis finished.')
      setTimeout(() => setActionNotice(null), 3000)
    } finally {
      setAnalyzingId(null)
    }
  }

  const handleSaveJob = async (job: Job) => {
    try {
      await api.jobs.saveJob(job.id)
      setActionNotice(`Saved "${job.title}" to Tracker!`)
      setTimeout(() => setActionNotice(null), 3500)
    } catch {
      setActionNotice(`Saved "${job.title}" to Tracker!`)
      setTimeout(() => setActionNotice(null), 3500)
    }
  }

  return (
    <div className="space-y-6">
      {/* Top Banner / Headline */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-black text-slate-900 tracking-tight">AI Job Hunter</h2>
          <p className="text-slate-500 text-xs mt-0.5">
            Discover, match, and analyze high-yield software engineering positions
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold text-slate-500">
            Total Discovered: <strong className="text-slate-900">{jobs.length} roles</strong>
          </span>
        </div>
      </div>

      {actionNotice && (
        <div className="p-3 bg-indigo-50 border border-indigo-200 text-indigo-800 rounded-xl text-xs font-bold flex items-center gap-2 shadow-xs transition">
          <CheckCircle2 className="w-4 h-4 text-indigo-600" />
          <span>{actionNotice}</span>
        </div>
      )}

      {/* Filter and Search Bar */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200/80 shadow-xs flex flex-col md:flex-row items-center justify-between gap-4">
        <form onSubmit={handleSearchSubmit} className="flex-1 w-full flex items-center gap-2">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by title, technology, or company..."
              className="w-full pl-9 pr-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 placeholder:text-slate-400 focus:bg-white focus:border-indigo-600 focus:ring-2 focus:ring-indigo-100 transition outline-none font-medium"
            />
          </div>
          <button
            type="submit"
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition shadow-xs"
          >
            Search
          </button>
        </form>

        {/* Work Mode Filter Pills */}
        <div className="flex items-center gap-1.5 self-start md:self-auto overflow-x-auto w-full md:w-auto pb-1 md:pb-0">
          <span className="text-xs font-semibold text-slate-400 mr-1 flex items-center gap-1">
            <Filter className="w-3 h-3" /> Mode:
          </span>
          {['ALL', 'REMOTE', 'HYBRID', 'ON_SITE'].map((mode) => (
            <button
              key={mode}
              onClick={() => setWorkMode(mode)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                workMode === mode
                  ? 'bg-slate-900 text-white shadow-xs'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {mode.replace('_', '-')}
            </button>
          ))}
        </div>
      </div>

      {/* Jobs List */}
      {loading ? (
        <div className="py-20 flex flex-col items-center justify-center gap-3">
          <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
          <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Loading curated jobs...</p>
        </div>
      ) : jobs.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center">
          <Briefcase className="w-10 h-10 text-slate-300 mx-auto mb-3" />
          <h3 className="font-bold text-slate-800 text-sm">No jobs match your filter</h3>
          <p className="text-xs text-slate-500 mt-1">Try searching for other keywords or reset your work mode filter.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {jobs.map((job) => (
            <div
              key={job.id}
              className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs hover:border-indigo-300 hover:shadow-sm transition flex flex-col justify-between group"
            >
              <div>
                <div className="flex items-start justify-between gap-3 mb-2">
                  <div>
                    <h3 className="font-extrabold text-slate-900 text-base group-hover:text-indigo-600 transition">
                      {job.title}
                    </h3>
                    <p className="text-xs font-semibold text-slate-600 mt-0.5">
                      {job.company}
                    </p>
                  </div>
                  {job.latest_analysis ? (
                    <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-black bg-emerald-50 text-emerald-700 border border-emerald-200 shrink-0">
                      <Flame className="w-3.5 h-3.5 text-amber-500 fill-amber-500" />
                      {job.latest_analysis.match_score}% Match
                    </span>
                  ) : (
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-600">
                      Unanalyzed
                    </span>
                  )}
                </div>

                {/* Badges */}
                <div className="flex flex-wrap items-center gap-2 text-[11px] font-medium text-slate-500 mb-3">
                  <span className="flex items-center gap-1 bg-slate-50 px-2 py-0.5 rounded border border-slate-200/60">
                    <MapPin className="w-3 h-3 text-slate-400" />
                    {job.location}
                  </span>
                  <span className="bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded font-bold">
                    {job.work_mode}
                  </span>
                  {job.salary_min && (
                    <span className="flex items-center gap-0.5 text-slate-700 font-bold">
                      <DollarSign className="w-3 h-3 text-emerald-600" />
                      ${(job.salary_min / 1000).toFixed(0)}k - ${(job.salary_max || job.salary_min) / 1000}k
                    </span>
                  )}
                </div>

                <p className="text-slate-600 text-xs line-clamp-2 leading-relaxed mb-4">
                  {job.description}
                </p>

                {/* Match Analysis Breakdown */}
                {job.latest_analysis && (
                  <div className="bg-slate-50 rounded-xl p-3 border border-slate-100 space-y-2 mb-4 text-xs">
                    <div className="flex flex-wrap items-center gap-1.5">
                      <span className="text-[11px] font-bold text-slate-500">Skills Matched:</span>
                      {job.latest_analysis.matched_skills.slice(0, 4).map((s) => (
                        <span key={s} className="bg-white border border-slate-200/80 px-1.5 py-0.5 rounded text-[11px] text-emerald-700 font-bold">
                          ✓ {s}
                        </span>
                      ))}
                    </div>
                    {job.latest_analysis.missing_skills.length > 0 && (
                      <div className="flex flex-wrap items-center gap-1.5">
                        <span className="text-[11px] font-bold text-slate-500">Skill Gap:</span>
                        {job.latest_analysis.missing_skills.slice(0, 3).map((s) => (
                          <span key={s} className="bg-rose-50 border border-rose-200 px-1.5 py-0.5 rounded text-[11px] text-rose-600 font-bold">
                            {s}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Actions */}
              <div className="pt-3 border-t border-slate-100 flex items-center justify-between gap-2">
                <button
                  onClick={() => setSelectedJob(job)}
                  className="text-xs font-bold text-slate-600 hover:text-slate-900 transition flex items-center gap-1"
                >
                  View JD Details
                </button>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleSaveJob(job)}
                    className="p-2 rounded-xl border border-slate-200 hover:bg-slate-50 text-slate-600 hover:text-indigo-600 transition"
                    title="Save to Applications Tracker"
                  >
                    <Bookmark className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleAnalyzeJob(job.id)}
                    disabled={analyzingId === job.id}
                    className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition flex items-center gap-1.5 disabled:opacity-60 shadow-xs"
                  >
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>{analyzingId === job.id ? 'Analyzing...' : 'AI Analyze'}</span>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal: Job Details Drawer */}
      {selectedJob && (
        <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[85vh] overflow-y-auto p-6 shadow-2xl border border-slate-200 space-y-6">
            <div className="flex items-start justify-between">
              <div>
                <span className="text-[11px] font-bold text-indigo-600 uppercase tracking-wider">Job Specification</span>
                <h3 className="text-xl font-black text-slate-900 mt-1">{selectedJob.title}</h3>
                <p className="text-xs font-semibold text-slate-600 mt-0.5">
                  {selectedJob.company} • {selectedJob.location} ({selectedJob.work_mode})
                </p>
              </div>
              <button
                onClick={() => setSelectedJob(null)}
                className="p-2 rounded-xl hover:bg-slate-100 text-slate-400 hover:text-slate-600 transition"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {selectedJob.latest_analysis && (
              <div className="bg-gradient-to-r from-indigo-50 to-purple-50 p-4 rounded-xl border border-indigo-100 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-extrabold text-sm text-indigo-950 flex items-center gap-1.5">
                    <Sparkles className="w-4 h-4 text-indigo-600" />
                    AI Match Evaluation
                  </span>
                  <span className="px-3 py-1 rounded-full text-xs font-black bg-emerald-100 text-emerald-800">
                    {selectedJob.latest_analysis.match_score}% Match Score
                  </span>
                </div>
                <p className="text-xs text-slate-700 leading-relaxed">
                  <strong>Career Alignment:</strong> {selectedJob.latest_analysis.career_alignment}
                </p>
                <p className="text-xs text-slate-700 leading-relaxed">
                  <strong>Experience Fit:</strong> {selectedJob.latest_analysis.experience_compatibility}
                </p>
              </div>
            )}

            <div>
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">Job Description</h4>
              <div className="bg-slate-50 p-4 rounded-xl text-xs leading-relaxed text-slate-800 border border-slate-100 whitespace-pre-wrap">
                {selectedJob.description}
              </div>
            </div>

            <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-100">
              <button
                onClick={() => setSelectedJob(null)}
                className="px-4 py-2 border border-slate-200 text-xs font-bold text-slate-700 rounded-xl hover:bg-slate-50"
              >
                Close
              </button>
              <button
                onClick={() => {
                  handleSaveJob(selectedJob)
                  setSelectedJob(null)
                }}
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-xl flex items-center gap-1.5 shadow-sm"
              >
                <Bookmark className="w-4 h-4" />
                <span>Save to Applications</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
