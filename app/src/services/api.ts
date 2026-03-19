import { reactive } from 'vue'
import axios from 'axios'
import type { Vendor, School, Distribution, Alert, Document } from './localStorage'

export const globalState = reactive({
  vendors: [] as Vendor[],
  schools: [] as School[],
  distributions: [] as Distribution[],
  alerts: [] as Alert[],
  documents: [] as Document[]
})

let isInitialized = false

export async function seedData() {
  if (isInitialized) return
  try {
    const res = await axios.get('/api/data')
    Object.assign(globalState, res.data)
    isInitialized = true
  } catch (err) {
    console.error('Failed to load initial data from backend', err)
  }
}

export function getData() {
  return globalState
}

export async function saveData(data: any) {
  try {
    await axios.post('/api/data', data)
    // Synchronize global state
    Object.assign(globalState, data)
  } catch (err) {
    console.error('Failed to save data to backend', err)
  }
}

// Re-export types from localStorage for now, since views import them from api.ts
export type { Vendor, School, Distribution, Alert, Document }
