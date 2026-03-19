import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export interface User {
  id: string
  name: string
  email: string
  role: 'vendor' | 'regulator'
  avatar: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => !!user.value)

  async function login(email: string, _password: string): Promise<boolean> {
    try {
      const res = await axios.post('/api/auth/login', { email, password: _password })
      user.value = res.data
      localStorage.setItem('kawalmbg_user', JSON.stringify(user.value))
      return true
    } catch (e) {
      return false
    }
  }

  function logout() {
    user.value = null
    localStorage.removeItem('kawalmbg_user')
  }

  function loadFromStorage() {
    const stored = localStorage.getItem('kawalmbg_user')
    if (stored) {
      user.value = JSON.parse(stored)
    }
  }

  loadFromStorage()

  return { user, isAuthenticated, login, logout, loadFromStorage }
})
