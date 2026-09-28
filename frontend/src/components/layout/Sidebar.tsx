import React from 'react'
import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard,
  Briefcase,
  Send,
  Linkedin,
  UserCheck,
  Github,
  Bot,
  BarChart3,
  CreditCard,
  LogOut,
  Sparkles,
} from 'lucide-react'
import { useAuth } from '@/context/AuthContext'

const navigationItems = [
  { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { name: 'AI Job Hunter', path: '/jobs', icon: Briefcase },
  { name: 'Applications', path: '/applications', icon: Send },
  { name: 'LinkedIn Content', path: '/linkedin', icon: Linkedin },
  { name: 'Profile Health', path: '/profile', icon: UserCheck },
  { name: 'GitHub Monitor', path: '/github', icon: Github },
  { name: 'AI Agents', path: '/agents', icon: Bot },
  { name: 'Career Analytics', path: '/analytics', icon: BarChart3 },
  { name: 'Billing & Plans', path: '/billing', icon: CreditCard },
]

export const Sidebar: React.FC = () => {
  const { user, logout } = useAuth()

  return (
    <aside className="w-64 bg-white border-r border-slate-200/80 flex flex-col h-screen fixed left-0 top-0 z-30 shadow-sm">
      {/* Brand Header */}
      <div className="h-16 flex items-center px-6 border-b border-slate-100 gap-3">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-cyan-500 flex items-center justify-center text-white shadow-md shadow-indigo-100">
          <Sparkles className="w-5 h-5" />
        </div>
        <div>
          <span className="font-extrabold text-base tracking-tight text-slate-900 block leading-tight">
            CareerPilot<span className="text-indigo-600">.AI</span>
          </span>
          <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-widest block">
            Career OS
          </span>
        </div>
      </div>

      {/* Workspace Tag */}
      {user?.tenant && (
        <div className="px-6 py-2.5 bg-slate-50/70 border-b border-slate-100">
          <p className="text-[11px] font-medium text-slate-500 truncate">
            Workspace: <strong className="text-slate-800 font-semibold">{user.tenant.name}</strong>
          </p>
        </div>
      )}

      {/* Nav Menu */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {navigationItems.map((item) => {
          const Icon = item.icon
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                  isActive
                    ? 'bg-indigo-50 text-indigo-700 shadow-sm border border-indigo-100/60 font-bold'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`
              }
            >
              {({ isActive }) => (
                <>
                  <Icon className={`w-4 h-4 transition ${isActive ? 'text-indigo-600' : 'text-slate-400'}`} />
                  <span>{item.name}</span>
                </>
              )}
            </NavLink>
          )
        })}
      </nav>

      {/* Footer / User Profile */}
      <div className="p-3 border-t border-slate-100 bg-slate-50/40">
        <div className="flex items-center justify-between p-2 rounded-xl bg-white border border-slate-200/60 shadow-xs">
          <div className="flex items-center gap-2.5 overflow-hidden">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-600 text-white font-bold text-xs flex items-center justify-center shrink-0">
              {user?.first_name ? user.first_name[0] : (user?.email ? user.email[0].toUpperCase() : 'U')}
            </div>
            <div className="overflow-hidden">
              <p className="text-xs font-bold text-slate-800 truncate">
                {user?.full_name || user?.email || 'Demo User'}
              </p>
              <p className="text-[10px] text-slate-500 truncate">{user?.email || 'Signed in'}</p>
            </div>
          </div>
          <button
            onClick={logout}
            title="Log out"
            className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>
  )
}
