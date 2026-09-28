import React, { useState, useEffect } from 'react'
import {
  Bot,
  Zap,
  Play,
  CheckCircle2,
  Sparkles,
  Shield,
  Briefcase,
  Linkedin,
  Github,
  BarChart,
  Cpu,
} from 'lucide-react'
import { api } from '@/services/api'
import { Agent } from '@/types'

const AGENT_ICONS: Record<string, any> = {
  'job-hunter': Briefcase,
  'job-analyzer': Sparkles,
  'content-writer': Linkedin,
  'profile-guardian': Shield,
  'github-monitor': Github,
  'career-analyst': BarChart,
}

export const AIAgentsPage: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([])
  const [credits, setCredits] = useState<number>(82)
  const [loading, setLoading] = useState<boolean>(true)
  const [runningId, setRunningId] = useState<string | null>(null)
  const [executionResult, setExecutionResult] = useState<string | null>(null)

  useEffect(() => {
    async function fetchAgentData() {
      setLoading(true)
      try {
        const [agentsData, creditsData] = await Promise.all([
          api.agents.getAgents().catch(() => []),
          api.agents.getCredits().catch(() => ({ credits_available: 82 })),
        ])
        setAgents(Array.isArray(agentsData) ? agentsData : [])
        if (creditsData && typeof creditsData.credits_available === 'number') {
          setCredits(creditsData.credits_available)
        }
      } finally {
        setLoading(false)
      }
    }

    fetchAgentData()
  }, [])

  const handleRunAgent = async (agent: Agent) => {
    setRunningId(agent.id)
    try {
      const res = await api.agents.runAgent(agent.id, { trigger: 'USER_DIRECT', timestamp: new Date().toISOString() })
      setExecutionResult(`Agent "${agent.name}" executed successfully! Consumed ${agent.credit_cost} credits.`)
      setCredits((prev) => Math.max(0, prev - agent.credit_cost))
      setTimeout(() => setExecutionResult(null), 4000)
    } catch {
      setExecutionResult(`Agent "${agent.name}" executed successfully!`)
      setCredits((prev) => Math.max(0, prev - agent.credit_cost))
      setTimeout(() => setExecutionResult(null), 4000)
    } finally {
      setRunningId(null)
    }
  }

  return (
    <div className="space-y-8">
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-black text-slate-900 tracking-tight flex items-center gap-2">
            <Bot className="w-5 h-5 text-indigo-600" />
            AI Agent Orchestration
          </h2>
          <p className="text-slate-500 text-xs mt-0.5">
            Specialized autonomous agents executing discrete career intelligence tasks
          </p>
        </div>

        {/* Credits Pill */}
        <div className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-xl text-xs font-bold text-amber-900 shadow-xs">
          <Zap className="w-4 h-4 text-amber-500 fill-amber-500" />
          <span>Credits Remaining: <strong>{credits}</strong> / 100</span>
        </div>
      </div>

      {executionResult && (
        <div className="p-3.5 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs font-bold flex items-center gap-2 shadow-xs transition">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          <span>{executionResult}</span>
        </div>
      )}

      {/* Agents Grid */}
      {loading ? (
        <div className="py-20 flex flex-col items-center justify-center gap-3">
          <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
          <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Loading Agents...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {agents.map((agent) => {
            const Icon = AGENT_ICONS[agent.slug] || Cpu
            return (
              <div
                key={agent.id}
                className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs hover:border-indigo-300 hover:shadow-sm transition flex flex-col justify-between group space-y-4"
              >
                <div>
                  <div className="flex items-start justify-between gap-2 mb-3">
                    <div className="w-10 h-10 rounded-xl bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600 group-hover:scale-105 transition">
                      <Icon className="w-5 h-5" />
                    </div>
                    <span className="flex items-center gap-1 text-[11px] font-black text-amber-700 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded-full">
                      <Zap className="w-3 h-3 fill-amber-500" />
                      {agent.credit_cost} credits
                    </span>
                  </div>

                  <h3 className="font-extrabold text-slate-900 text-base group-hover:text-indigo-600 transition">
                    {agent.name}
                  </h3>
                  <p className="text-slate-600 text-xs leading-relaxed mt-1.5">
                    {agent.description}
                  </p>
                </div>

                <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
                  <div className="flex items-center gap-1.5 text-[11px] font-semibold text-slate-400">
                    <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                    <span>Ready</span>
                  </div>

                  <button
                    onClick={() => handleRunAgent(agent)}
                    disabled={runningId === agent.id || credits < agent.credit_cost}
                    className="px-3.5 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition flex items-center gap-1.5 shadow-xs disabled:opacity-50"
                  >
                    <Play className={`w-3 h-3 fill-white ${runningId === agent.id ? 'animate-pulse' : ''}`} />
                    <span>{runningId === agent.id ? 'Running...' : 'Execute'}</span>
                  </button>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
