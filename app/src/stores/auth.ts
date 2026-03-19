import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

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

  function login(email: string, _password: string): boolean {
    if (email.includes('regulator')) {
      user.value = {
        id: '1',
        name: 'Moni Roy',
        email,
        role: 'regulator',
        avatar: 'https://i.pravatar.cc/80?u=regulator',
      }
      localStorage.setItem('kawalmbg_user', JSON.stringify(user.value))
      return true
    } else if (email.includes('vendor')) {
      user.value = {
        id: '2',
        name: 'Moni Roy',
        email,
        role: 'vendor',
        avatar: 'https://i.pravatar.cc/80?u=vendor',
      }
      localStorage.setItem('kawalmbg_user', JSON.stringify(user.value))
      return true
    }
    return false
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
