import axios from 'axios'

export const AUTH_TOKEN_STORAGE_KEY = 'kawalmbg_token'
export const AUTH_USER_STORAGE_KEY = 'kawalmbg_user'
const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL as string | undefined)?.trim()

export const http = axios.create({
  baseURL: apiBaseUrl || undefined,
})

export function getAuthToken() {
  return localStorage.getItem(AUTH_TOKEN_STORAGE_KEY)
}

export function setAuthToken(token: string) {
  localStorage.setItem(AUTH_TOKEN_STORAGE_KEY, token)
}

export function clearStoredSession() {
  localStorage.removeItem(AUTH_TOKEN_STORAGE_KEY)
  localStorage.removeItem(AUTH_USER_STORAGE_KEY)
}

http.interceptors.request.use((config) => {
  const token = getAuthToken()
  if (token) {
    config.headers = config.headers ?? {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
