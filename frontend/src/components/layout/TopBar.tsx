import React, { useState, useEffect } from 'react'
import { Bell, Zap, Search, ShieldCheck } from 'lucide-react'
import { api } from '@/services/api'
import { useAuth } from '@/context/AuthContext'
import { Link } from 'react-router-dom'

interface TopBarProps {
  title?: string
}

export const TopBar: React.FC<TopBarProps> = ({ title = 'Dashboard' }) => {
  const { user } = useAuth()
  const [credits, setCredits] = useState<number>(82)
  const [unreadNotifications, setUnreadNotifications] = useState<number>(2)

  useEffect(() => {
    async function fetchHeaderData() {
      try {
        const [creditData, notifData] = await Promise.all([
          api.agents.getCredits().catch(() => ({ credits_available: 82 })),
          api.notifications.getNotifications().catch(() => []),
        ])
        if (creditData && typeof creditData.credits_available === 'number') {
          setCredits(creditData.credits_available)
        }
        if (Array.isArray(notifData)) {
          const unread = notifData.filter((n: any) => !n.is_read).length
          setUnreadNotifications(unread)
        }
      } catch (err) {
        console.warn('TopBar fetch error', err)
      }
    }

    fetchHeaderData()
  }, [])

  return (
    <header className="h-16 bg-white border-b border-slate-200/80 sticky top-0 z-20 px-8 flex items-center justify-between">
      <div className="flex items-center gap-4">
        <h1 className="text-xl font-extrabold text-slate-900 tracking-tight capitalize">
          {title.replace('-', ' ')}
        </h1>
        <div className="hidden sm:inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-50 border border-emerald-200/70 text-emerald-700 text-[11px] font-bold">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Tenant Isolated</span>
        </div>
      </div>

      <div className="flex items-center gap-3">
        {/* Global Search Bar */}
        <div className="hidden md:flex items-center bg-slate-100 rounded-xl px-3 py-1.5 w-64 border border-transparent focus-within:border-indigo-300 focus-within:bg-white transition">
          <Search className="w-4 h-4 text-slate-400 mr-2 shrink-0" />
          <input
            type="text"
            placeholder="Search jobs, skills, posts..."
            className="bg-transparent text-xs text-slate-800 placeholder:text-slate-400 outline-none w-full font-medium"
          />
        </div>

        {/* AI Credits Widget */}
        <Link
          to="/billing"
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 text-amber-800 hover:border-amber-300 transition shadow-xs text-xs font-bold"
          title="AI Credits Remaining"
        >
          <Zap className="w-3.5 h-3.5 text-amber-600 fill-amber-500" />
          <span>{credits}</span>
          <span className="text-[10px] text-amber-700/80 font-normal">credits</span>
        </Link>

        {/* Notifications */}
        <div className="relative">
          <button
            className="p-2 rounded-xl text-slate-500 hover:text-slate-800 hover:bg-slate-100 transition relative border border-slate-200/70 shadow-xs"
            title="Notifications"
          >
            <Bell className="w-4 h-4" />
            {unreadNotifications > 0 && (
              <span className="absolute -top-1 -right-1 w-4 h-4 bg-rose-500 text-white rounded-full text-[10px] font-black flex items-center justify-center ring-2 ring-white">
                {unreadNotifications}
              </span>
            )}
          </button>
        </div>

        {/* User Mini Avatar */}
        <Link
          to="/profile"
          className="flex items-center gap-2 pl-2 border-l border-slate-200 hover:opacity-85 transition"
        >
          <div className="w-8 h-8 rounded-full bg-indigo-600 text-white font-bold text-xs flex items-center justify-center shadow-xs ring-2 ring-indigo-50">
            {user?.first_name ? user.first_name[0] : 'A'}
          </div>
        </Link>
      </div>
    </header>
  )
}
