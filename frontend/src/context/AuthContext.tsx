import React, { createContext, useContext, useState, useEffect } from 'react'
import { User } from '@/types'
import { api } from '@/services/api'

interface AuthContextType {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, firstName?: string, lastName?: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('access_token'))
  const [isLoading, setIsLoading] = useState<boolean>(true)

  useEffect(() => {
    async function loadUser() {
      const storedToken = localStorage.getItem('access_token')
      if (storedToken) {
        try {
          const userData = await api.auth.me()
          setUser(userData)
        } catch (error) {
          console.warn('Failed to load user session:', error)
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          setToken(null)
          setUser(null)
        }
      }
      setIsLoading(false)
    }

    loadUser()
  }, [])

  const login = async (email: string, password: string) => {
    setIsLoading(true)
    try {
      const data = await api.auth.login({ email, password })
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
      setToken(data.access_token)
      setUser(data.user)
    } finally {
      setIsLoading(false)
    }
  }

  const register = async (email: string, password: string, firstName?: string, lastName?: string) => {
    setIsLoading(true)
    try {
      const data = await api.auth.register({ email, password, first_name: firstName, last_name: lastName })
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
      setToken(data.access_token)
      setUser(data.user)
    } finally {
      setIsLoading(false)
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!token,
        isLoading,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
