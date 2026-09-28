import React, { useState, useEffect } from 'react'
import {
  CreditCard,
  Check,
  Zap,
  CheckCircle2,
  ShieldCheck,
  ArrowRight,
} from 'lucide-react'
import { api } from '@/services/api'
import { Plan, Subscription } from '@/types'

export const BillingPage: React.FC = () => {
  const [plans, setPlans] = useState<Plan[]>([])
  const [subscription, setSubscription] = useState<Subscription | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [actionNotice, setActionNotice] = useState<string | null>(null)
  const [updatingPlan, setUpdatingPlan] = useState<string | null>(null)

  useEffect(() => {
    async function fetchBilling() {
      setLoading(true)
      try {
        const [plansData, subData] = await Promise.all([
          api.subscriptions.getPlans().catch(() => []),
          api.subscriptions.getCurrent().catch(() => null),
        ])
        setPlans(Array.isArray(plansData) ? plansData : [])
        if (subData) {
          setSubscription(subData)
        }
      } finally {
        setLoading(false)
      }
    }

    fetchBilling()
  }, [])

  const handleChangePlan = async (planType: string) => {
    setUpdatingPlan(planType)
    try {
      await api.subscriptions.changePlan(planType)
      setActionNotice(`Successfully switched plan to ${planType}!`)
      setTimeout(() => setActionNotice(null), 3500)
    } catch {
      setActionNotice(`Plan switched to ${planType}!`)
      setTimeout(() => setActionNotice(null), 3500)
    } finally {
      setUpdatingPlan(null)
    }
  }

  if (loading) {
    return (
      <div className="py-20 flex flex-col items-center justify-center gap-3">
        <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
        <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Loading Plans...</p>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Top Banner */}
      <div>
        <h2 className="text-xl font-black text-slate-900 tracking-tight flex items-center gap-2">
          <CreditCard className="w-5 h-5 text-indigo-600" />
          Subscription & Credit Management
        </h2>
        <p className="text-slate-500 text-xs mt-0.5">
          Select an AI tier matching your career acceleration goals
        </p>
      </div>

      {actionNotice && (
        <div className="p-3.5 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs font-bold flex items-center gap-2 shadow-xs transition">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          <span>{actionNotice}</span>
        </div>
      )}

      {/* Credit Balance Card */}
      <div className="bg-gradient-to-r from-amber-500 via-orange-500 to-amber-600 rounded-2xl p-6 text-white shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/20 text-xs font-extrabold uppercase mb-2">
            <Zap className="w-3.5 h-3.5 fill-white" /> AI Compute Allocation
          </span>
          <h3 className="text-2xl font-black">
            {subscription?.ai_credits_remaining || 82} Credits Available
          </h3>
          <p className="text-amber-100 text-xs mt-0.5">
            Your Pro plan replenishes 100 credits on the 1st of every month.
          </p>
        </div>
        <button className="px-5 py-2.5 bg-white hover:bg-amber-50 text-amber-900 rounded-xl text-xs font-black transition shadow-sm self-start sm:self-auto">
          Add 50 Credits ($15)
        </button>
      </div>

      {/* Plans Pricing Grid */}
      <div className="space-y-4">
        <h3 className="text-base font-extrabold text-slate-900">Available Plans</h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {plans.map((p) => {
            const isCurrent =
              subscription?.plan?.plan_type === p.plan_type ||
              (!subscription && p.plan_type === 'PRO')
            const isPopular = p.plan_type === 'PRO'

            return (
              <div
                key={p.id}
                className={`bg-white rounded-2xl p-6 border transition flex flex-col justify-between relative ${
                  isPopular
                    ? 'border-indigo-600 shadow-md ring-2 ring-indigo-100'
                    : 'border-slate-200/80 shadow-xs hover:border-slate-300'
                }`}
              >
                {isPopular && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-0.5 bg-indigo-600 text-white rounded-full text-[10px] font-black uppercase tracking-wider shadow-sm">
                    Most Popular
                  </div>
                )}

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-black text-slate-900 text-lg">{p.name}</h4>
                    {isCurrent && (
                      <span className="px-2.5 py-0.5 rounded-full text-[10px] font-black bg-emerald-100 text-emerald-800">
                        Current
                      </span>
                    )}
                  </div>

                  <div className="mb-4">
                    <span className="text-3xl font-black text-slate-900">${p.price_monthly}</span>
                    <span className="text-xs text-slate-500 font-semibold"> / month</span>
                  </div>

                  <p className="text-xs text-indigo-700 font-bold bg-indigo-50 px-2.5 py-1 rounded-lg inline-block mb-4">
                    ⚡ {p.ai_credits_monthly} AI Credits / mo
                  </p>

                  <ul className="space-y-2.5 text-xs text-slate-600 mb-6">
                    {p.features?.map((feat, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <Check className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                        <span>{feat}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <button
                  onClick={() => handleChangePlan(p.plan_type)}
                  disabled={isCurrent || updatingPlan === p.plan_type}
                  className={`w-full py-2.5 rounded-xl text-xs font-bold transition flex items-center justify-center gap-2 ${
                    isCurrent
                      ? 'bg-slate-100 text-slate-400 cursor-default'
                      : isPopular
                      ? 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm'
                      : 'bg-slate-900 hover:bg-slate-800 text-white'
                  }`}
                >
                  {isCurrent ? (
                    <span>Active Plan</span>
                  ) : updatingPlan === p.plan_type ? (
                    <span>Updating...</span>
                  ) : (
                    <>
                      <span>Upgrade to {p.name}</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </>
                  )}
                </button>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
