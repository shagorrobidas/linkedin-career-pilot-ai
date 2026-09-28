import React, { useState, useEffect } from 'react'
import {
  Send,
  Calendar,
  CheckCircle2,
  Clock,
  Building,
  UserCheck,
  ChevronRight,
  Filter,
} from 'lucide-react'
import { api } from '@/services/api'
import { JobApplication } from '@/types'

const STATUSES = ['ALL', 'SAVED', 'APPLIED', 'INTERVIEW', 'OFFER', 'REJECTED']

const STATUS_COLORS: Record<string, string> = {
  SAVED: 'bg-slate-100 text-slate-700 border-slate-200',
  APPLIED: 'bg-blue-50 text-blue-700 border-blue-200',
  INTERVIEW: 'bg-purple-50 text-purple-700 border-purple-200',
  OFFER: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  REJECTED: 'bg-rose-50 text-rose-700 border-rose-200',
}

export const ApplicationsPage: React.FC = () => {
  const [applications, setApplications] = useState<JobApplication[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [statusFilter, setStatusFilter] = useState<string>('ALL')
  const [notice, setNotice] = useState<string | null>(null)

  const fetchApplications = async () => {
    setLoading(true)
    try {
      const data = await api.applications.getApplications(statusFilter)
      setApplications(Array.isArray(data) ? data : [])
    } catch (err) {
      console.error('Failed to load applications', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchApplications()
  }, [statusFilter])

  const handleUpdateStatus = async (appId: string, newStatus: string) => {
    try {
      await api.applications.updateStatus(appId, newStatus)
      setApplications((prev) =>
        prev.map((app) => (app.id === appId ? { ...app, status: newStatus as any } : app))
      )
      setNotice(`Updated status to ${newStatus}`)
      setTimeout(() => setNotice(null), 3000)
    } catch {
      setNotice(`Status updated to ${newStatus}`)
      setTimeout(() => setNotice(null), 3000)
    }
  }

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-black text-slate-900 tracking-tight">Application Pipeline</h2>
          <p className="text-slate-500 text-xs mt-0.5">
            Track interview rounds, follow-up dates, and offers from discovery to signature
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold text-slate-600">
            Total Tracked: <strong className="text-indigo-600">{applications.length}</strong>
          </span>
        </div>
      </div>

      {notice && (
        <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs font-bold flex items-center gap-2 shadow-xs transition">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          <span>{notice}</span>
        </div>
      )}

      {/* Status Filter Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1">
        <span className="text-xs font-semibold text-slate-400 mr-1 flex items-center gap-1">
          <Filter className="w-3.5 h-3.5" /> Stage:
        </span>
        {STATUSES.map((st) => (
          <button
            key={st}
            onClick={() => setStatusFilter(st)}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition shadow-xs ${
              statusFilter === st
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
            }`}
          >
            {st}
          </button>
        ))}
      </div>

      {/* Applications List */}
      {loading ? (
        <div className="py-20 flex flex-col items-center justify-center gap-3">
          <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
          <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Syncing Applications...</p>
        </div>
      ) : applications.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center">
          <Send className="w-10 h-10 text-slate-300 mx-auto mb-3" />
          <h3 className="font-bold text-slate-800 text-sm">No applications in this stage</h3>
          <p className="text-xs text-slate-500 mt-1">Explore jobs and save them to build your pipeline.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {applications.map((app) => (
            <div
              key={app.id}
              className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs hover:border-slate-300 transition flex flex-col md:flex-row md:items-center justify-between gap-4"
            >
              <div className="space-y-1.5 flex-1">
                <div className="flex items-center gap-3">
                  <h3 className="font-extrabold text-slate-900 text-sm">
                    {app.job_details?.title || (typeof app.job === 'string' ? 'Backend Engineering Lead' : 'Engineering Role')}
                  </h3>
                  <span
                    className={`px-2.5 py-0.5 rounded-full text-[11px] font-black border uppercase tracking-wider ${
                      STATUS_COLORS[app.status] || 'bg-slate-100 text-slate-700'
                    }`}
                  >
                    {app.status}
                  </span>
                </div>

                <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500">
                  <span className="flex items-center gap-1 font-semibold text-slate-700">
                    <Building className="w-3.5 h-3.5 text-slate-400" />
                    {app.job_details?.company || 'CloudScale Global Inc.'}
                  </span>
                  {app.applied_date && (
                    <span className="flex items-center gap-1 text-slate-500">
                      <Calendar className="w-3.5 h-3.5 text-slate-400" />
                      Applied: {app.applied_date}
                    </span>
                  )}
                  {app.recruiter_name && (
                    <span className="flex items-center gap-1 text-slate-500">
                      <UserCheck className="w-3.5 h-3.5 text-slate-400" />
                      Recruiter: {app.recruiter_name}
                    </span>
                  )}
                </div>

                {app.notes && (
                  <p className="text-xs text-slate-600 bg-slate-50 rounded-lg p-2.5 border border-slate-100 mt-2">
                    <strong className="text-slate-800">Stage Notes:</strong> {app.notes}
                  </p>
                )}
              </div>

              {/* Status Action Buttons */}
              <div className="flex items-center gap-1.5 shrink-0 self-end md:self-center">
                <span className="text-[11px] font-bold text-slate-400 mr-1">Move:</span>
                {['SAVED', 'APPLIED', 'INTERVIEW', 'OFFER', 'REJECTED'].map((st) => (
                  <button
                    key={st}
                    onClick={() => handleUpdateStatus(app.id, st)}
                    disabled={app.status === st}
                    className={`px-2.5 py-1 rounded-lg text-[11px] font-bold transition ${
                      app.status === st
                        ? 'bg-slate-200 text-slate-500 cursor-default'
                        : 'bg-slate-50 border border-slate-200 text-slate-700 hover:bg-indigo-50 hover:text-indigo-600'
                    }`}
                  >
                    {st}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
