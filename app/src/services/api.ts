import { reactive } from 'vue'
import type { Vendor, School, Distribution, DistributionAssessment, Alert, Document } from './localStorage'
import { clearStoredSession, getAuthToken, http } from './http'

export const globalState = reactive({
  vendors: [] as Vendor[],
  schools: [] as School[],
  distributions: [] as Distribution[],
  alerts: [] as Alert[],
  documents: [] as Document[]
})

let isInitialized = false

function applyState(data: Partial<typeof globalState>) {
  globalState.vendors = data.vendors ?? []
  globalState.schools = data.schools ?? []
  globalState.distributions = data.distributions ?? []
  globalState.alerts = data.alerts ?? []
  globalState.documents = data.documents ?? []
}

async function loadPublicData() {
  const res = await http.get('/api/public-data')
  applyState(res.data)
}

async function loadPrivateData() {
  const res = await http.get('/api/data')
  applyState(res.data)
}

export async function seedData(force = false) {
  if (isInitialized && !force) return
  try {
    if (getAuthToken()) {
      await loadPrivateData()
    } else {
      await loadPublicData()
    }
    isInitialized = true
  } catch (err: any) {
    if (getAuthToken() && err?.response?.status === 401) {
      clearStoredSession()
      await loadPublicData()
      isInitialized = true
      return
    }
    console.error('Failed to load initial data from backend', err)
  }
}

export function getData() {
  return globalState
}

export async function saveData(data: any) {
  try {
    const res = await http.post('/api/data', data)
    applyState(res.data)
  } catch (err: any) {
    if (err?.response?.status === 401) {
      clearStoredSession()
      await seedData(true)
    }
    console.error('Failed to save data to backend', err)
  }
}

// Re-export types from localStorage for now, since views import them from api.ts
export type { Vendor, School, Distribution, DistributionAssessment, Alert, Document }
