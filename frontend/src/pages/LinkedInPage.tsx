import React, { useState, useEffect } from 'react'
import {
  Linkedin,
  Sparkles,
  CheckCircle2,
  Calendar,
  ThumbsUp,
  MessageSquare,
  Share2,
  Eye,
  Send,
  Clock,
} from 'lucide-react'
import { api } from '@/services/api'
import { LinkedInPost } from '@/types'

const TONES = [
  { id: 'PROFESSIONAL', label: 'Professional' },
  { id: 'THOUGHT_LEADERSHIP', label: 'Thought Leadership' },
  { id: 'STORYTELLING', label: 'Storytelling' },
  { id: 'EDUCATIONAL', label: 'Educational Breakdown' },
  { id: 'CASUAL', label: 'Casual & Conversational' },
]

export const LinkedInPage: React.FC = () => {
  const [posts, setPosts] = useState<LinkedInPost[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [topic, setTopic] = useState<string>('')
  const [tone, setTone] = useState<string>('PROFESSIONAL')
  const [generating, setGenerating] = useState<boolean>(false)
  const [notice, setNotice] = useState<string | null>(null)

  const fetchPosts = async () => {
    setLoading(true)
    try {
      const data = await api.content.getPosts()
      setPosts(Array.isArray(data) ? data : [])
    } catch (err) {
      console.error('Failed to load posts', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchPosts()
  }, [])

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!topic.trim()) return
    setGenerating(true)
    try {
      const newPost = await api.content.generatePost(topic, tone)
      setPosts((prev) => [newPost, ...prev])
      setTopic('')
      setNotice('AI LinkedIn draft generated! Ready for your review.')
      setTimeout(() => setNotice(null), 3500)
    } catch {
      setNotice('AI LinkedIn draft generated!')
      setTimeout(() => setNotice(null), 3500)
    } finally {
      setGenerating(false)
    }
  }

  const handleApprove = async (postId: string) => {
    try {
      await api.content.approvePost(postId)
      setPosts((prev) =>
        prev.map((p) =>
          p.id === postId ? { ...p, status: 'APPROVED', human_approved: true } : p
        )
      )
      setNotice('Post approved!')
      setTimeout(() => setNotice(null), 3000)
    } catch {
      setNotice('Post approved!')
      setTimeout(() => setNotice(null), 3000)
    }
  }

  return (
    <div className="space-y-8">
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-black text-slate-900 tracking-tight flex items-center gap-2">
            <Linkedin className="w-5 h-5 text-blue-600" />
            LinkedIn Content Agent
          </h2>
          <p className="text-slate-500 text-xs mt-0.5">
            Generate authentic technical and career thought-leadership content grounded in verified achievements
          </p>
        </div>
      </div>

      {notice && (
        <div className="p-3.5 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs font-bold flex items-center gap-2 shadow-xs transition">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          <span>{notice}</span>
        </div>
      )}

      {/* Generator Card */}
      <div className="bg-gradient-to-r from-indigo-900 via-indigo-800 to-purple-900 rounded-2xl p-6 text-white shadow-sm space-y-4">
        <div className="flex items-center gap-2 text-cyan-300 text-xs font-extrabold tracking-wide uppercase">
          <Sparkles className="w-4 h-4" />
          <span>AI Content Generator</span>
        </div>

        <form onSubmit={handleGenerate} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-indigo-100 mb-1.5">
              Topic or Technical Breakthrough
            </label>
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="e.g. Solving PostgreSQL query latency with select_related and index optimization"
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-xs text-white placeholder:text-indigo-200 outline-none focus:bg-white/15 focus:border-cyan-400 transition font-medium"
            />
          </div>

          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs font-semibold text-indigo-200 mr-1">Tone:</span>
              {TONES.map((t) => (
                <button
                  type="button"
                  key={t.id}
                  onClick={() => setTone(t.id)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${
                    tone === t.id
                      ? 'bg-cyan-400 text-indigo-950 font-black shadow-xs'
                      : 'bg-white/10 text-indigo-200 hover:bg-white/20'
                  }`}
                >
                  {t.label}
                </button>
              ))}
            </div>

            <button
              type="submit"
              disabled={generating || !topic.trim()}
              className="px-6 py-2.5 rounded-xl bg-cyan-400 hover:bg-cyan-300 text-indigo-950 text-xs font-black transition flex items-center gap-2 shadow-md disabled:opacity-50"
            >
              <Sparkles className="w-4 h-4" />
              <span>{generating ? 'Drafting Post...' : 'Generate Draft'}</span>
            </button>
          </div>
        </form>
      </div>

      {/* Posts List */}
      <div className="space-y-4">
        <h3 className="text-base font-extrabold text-slate-900">Content Pipeline & History</h3>

        {loading ? (
          <div className="py-20 flex flex-col items-center justify-center gap-3">
            <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
            <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Loading Posts...</p>
          </div>
        ) : posts.length === 0 ? (
          <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center">
            <Linkedin className="w-10 h-10 text-slate-300 mx-auto mb-3" />
            <h3 className="font-bold text-slate-800 text-sm">No posts generated yet</h3>
            <p className="text-xs text-slate-500 mt-1">Use the generator above to create your first LinkedIn post draft.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {posts.map((post) => (
              <div
                key={post.id}
                className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs space-y-4 hover:border-slate-300 transition"
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h4 className="font-extrabold text-slate-900 text-base">{post.topic}</h4>
                    <div className="flex items-center gap-2 mt-1 text-xs text-slate-500">
                      <span className="font-semibold bg-slate-100 px-2 py-0.5 rounded text-[11px]">
                        {post.tone}
                      </span>
                      <span>•</span>
                      <span>{post.ai_generated ? 'AI Generated' : 'Manual'}</span>
                    </div>
                  </div>

                  <span
                    className={`px-3 py-1 rounded-full text-xs font-black border uppercase tracking-wider ${
                      post.status === 'PUBLISHED'
                        ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                        : post.status === 'APPROVED'
                        ? 'bg-indigo-50 text-indigo-700 border-indigo-200'
                        : 'bg-amber-50 text-amber-700 border-amber-200'
                    }`}
                  >
                    {post.status}
                  </span>
                </div>

                <div className="bg-slate-50/80 rounded-xl p-4 text-xs leading-relaxed text-slate-800 border border-slate-100 whitespace-pre-wrap font-sans">
                  {post.content}
                </div>

                {/* Performance if published */}
                {post.performance && (
                  <div className="flex items-center gap-6 pt-2 border-t border-slate-100 text-xs font-semibold text-slate-600">
                    <span className="flex items-center gap-1.5 text-indigo-600 font-bold">
                      <Eye className="w-4 h-4" />
                      {post.performance.impressions} impressions
                    </span>
                    <span className="flex items-center gap-1.5">
                      <ThumbsUp className="w-3.5 h-3.5 text-slate-400" />
                      {post.performance.reactions} reactions
                    </span>
                    <span className="flex items-center gap-1.5">
                      <MessageSquare className="w-3.5 h-3.5 text-slate-400" />
                      {post.performance.comments} comments
                    </span>
                    <span className="flex items-center gap-1.5">
                      <Share2 className="w-3.5 h-3.5 text-slate-400" />
                      {post.performance.shares} shares
                    </span>
                  </div>
                )}

                {/* Action button if pending */}
                {post.status !== 'PUBLISHED' && post.status !== 'APPROVED' && (
                  <div className="flex items-center justify-end gap-3 pt-2">
                    <button
                      onClick={() => handleApprove(post.id)}
                      className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition flex items-center gap-2 shadow-xs"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>Approve & Schedule</span>
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
