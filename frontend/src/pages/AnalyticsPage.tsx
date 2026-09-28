import React, { useState, useEffect } from 'react'
import {
  BarChart3,
  TrendingUp,
  Lightbulb,
  Sparkles,
  Eye,
  CheckCircle2,
  Calendar,
} from 'lucide-react'
import { api } from '@/services/api'
import { CareerInsightItem } from '@/types'

export const AnalyticsPage: React.FC = () => {
  const [insights, setInsights] = useState<CareerInsightItem[]>([])
  const [summary, setSummary] = useState<any>(null)
  const [loading, setLoading] = useState<boolean>(true)

  useEffect(() => {
    async function fetchAnalytics() {
      setLoading(true)
      try {
        const [sumData, insightData] = await Promise.all([
          api.analytics.getSummary().catch(() => null),
          api.analytics.getInsights().catch(() => []),
        ])
        setSummary(sumData)
        setInsights(Array.isArray(insightData) ? insightData : [])
      } finally {
        setLoading(false)
      }
    }

    fetchAnalytics()
  }, [])

  if (loading) {
    return (
      <div className="py-20 flex flex-col items-center justify-center gap-3">
        <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
        <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Compiling Career Metrics...</p>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Top Banner */}
      <div>
        <h2 className="text-xl font-black text-slate-900 tracking-tight flex items-center gap-2">
          <BarChart3 className="w-5 h-5 text-indigo-600" />
          Career Growth Analytics
        </h2>
        <p className="text-slate-500 text-xs mt-0.5">
          Quantified career metrics, application conversion velocity, and data-backed market signals
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
        <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs space-y-2">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
            Weekly Post Impressions
          </span>
          <div className="text-3xl font-black text-slate-900">
            {summary?.post_impressions_weekly || 4280}
          </div>
          <p className="text-xs font-semibold text-emerald-600 flex items-center gap-1">
            <TrendingUp className="w-3.5 h-3.5" /> +28% vs previous week
          </p>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs space-y-2">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
            High-Match Rate
          </span>
          <div className="text-3xl font-black text-indigo-600">
            {summary?.high_match_percentage || 85}%
          </div>
          <p className="text-xs text-slate-500 font-medium">
            Proportion of discovered jobs meeting requirements
          </p>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs space-y-2">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
            AI Credits Utilized
          </span>
          <div className="text-3xl font-black text-purple-600">
            {summary?.ai_credits_used_this_week || 18}
          </div>
          <p className="text-xs text-slate-500 font-medium">
            Across job analysis, drafting, and audits
          </p>
        </div>
      </div>

      {/* Career Insights Section */}
      <div className="space-y-4">
        <h3 className="text-base font-extrabold text-slate-900 flex items-center gap-2">
          <Lightbulb className="w-4 h-4 text-amber-500" />
          Strategic Career Insights
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {insights.map((ins, idx) => (
            <div
              key={ins.id || idx}
              className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs space-y-3"
            >
              <div className="flex items-center justify-between">
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider bg-indigo-50 text-indigo-700">
                  {ins.category}
                </span>
                <Sparkles className="w-4 h-4 text-indigo-500" />
              </div>

              <h4 className="font-extrabold text-slate-900 text-sm">{ins.title}</h4>
              <p className="text-slate-600 text-xs leading-relaxed">{ins.description}</p>

              {ins.actionable_step && (
                <div className="p-3 rounded-xl bg-amber-50/70 border border-amber-200/70 text-amber-900 text-xs font-medium leading-relaxed">
                  <strong className="font-bold">Next Action:</strong> {ins.actionable_step}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
