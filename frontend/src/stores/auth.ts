import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { seedData } from '@/services/api'
import { AUTH_USER_STORAGE_KEY, clearStoredSession, getAuthToken, http, setAuthToken } from '@/services/http'

export interface User {
  id: string
  name: string
  email: string
  role: 'vendor' | 'regulator' | 'super-admin'
  vendorId?: string | null
  isActive?: boolean
  createdAt?: string | null
  lastLoginAt?: string | null
  avatar: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const sessionChecked = ref(false)

  const isAuthenticated = computed(() => !!user.value && !!getAuthToken())

  async function login(email: string, _password: string): Promise<{ ok: true } | { ok: false; error: string }> {
    try {
      const res = await http.post('/api/auth/login', { email, password: _password })
      setAuthToken(res.data.token)
      user.value = res.data.user
      localStorage.setItem(AUTH_USER_STORAGE_KEY, JSON.stringify(user.value))
      sessionChecked.value = true
      await seedData(true)
      return { ok: true }
    } catch (e: any) {
      const message = e?.response?.data?.detail
      return {
        ok: false,
        error: typeof message === 'string' ? message : 'Login failed',
      }
    }
  }

  function clearSession() {
    user.value = null
    clearStoredSession()
    sessionChecked.value = true
  }

  function logout() {
    clearSession()
    void seedData(true)
  }

  function loadFromStorage() {
    const stored = localStorage.getItem(AUTH_USER_STORAGE_KEY)
    if (!stored || !getAuthToken()) {
      clearStoredSession()
      user.value = null
      sessionChecked.value = true
      return
    }

    try {
      user.value = JSON.parse(stored)
    } catch {
      clearSession()
    }
  }

  async function restoreSession(force = false) {
    if (!getAuthToken()) {
      clearSession()
      return false
    }
    if (sessionChecked.value && !force && user.value) {
      return true
    }

    if (!user.value) {
      loadFromStorage()
    }

    try {
      const res = await http.get('/api/auth/session')
      user.value = res.data
      localStorage.setItem(AUTH_USER_STORAGE_KEY, JSON.stringify(user.value))
      sessionChecked.value = true
      return true
    } catch {
      clearSession()
      return false
    }
  }

  loadFromStorage()

  return { user, isAuthenticated, login, logout, loadFromStorage, restoreSession }
})
