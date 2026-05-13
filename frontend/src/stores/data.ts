import { defineStore } from 'pinia'
import { reactive, ref } from 'vue'

import type { Alert, Distribution, Document, School, Vendor } from '@/types/domain'
import { clearStoredSession, getAuthToken, http } from '@/services/http'

type DatasetState = {
  vendors: Vendor[]
  schools: School[]
  distributions: Distribution[]
  alerts: Alert[]
  documents: Document[]
}

function createEmptyState(): DatasetState {
  return {
    vendors: [],
    schools: [],
    distributions: [],
    alerts: [],
    documents: [],
  }
}

export const useDataStore = defineStore('data', () => {
  const state = reactive<DatasetState>(createEmptyState())
  const initialized = ref(false)
  const loading = ref(false)
  const lastError = ref('')

  function applyState(data: Partial<DatasetState>) {
    state.vendors = data.vendors ?? []
    state.schools = data.schools ?? []
    state.distributions = data.distributions ?? []
    state.alerts = data.alerts ?? []
    state.documents = data.documents ?? []
  }

  async function loadPublicData() {
    const res = await http.get<DatasetState>('/api/public-data')
    applyState(res.data)
  }

  async function loadPrivateData() {
    const res = await http.get<DatasetState>('/api/data')
    applyState(res.data)
  }

  async function seed(force = false) {
    if (initialized.value && !force) return

    loading.value = true
    lastError.value = ''
    try {
      if (getAuthToken()) {
        await loadPrivateData()
      } else {
        await loadPublicData()
      }
      initialized.value = true
    } catch (err: any) {
      if (getAuthToken() && err?.response?.status === 401) {
        clearStoredSession()
        await loadPublicData()
        initialized.value = true
        return
      }
      lastError.value = 'Failed to load initial data from backend'
      console.error(lastError.value, err)
    } finally {
      loading.value = false
    }
  }

  async function save(payload: unknown) {
    try {
      const res = await http.post<DatasetState>('/api/data', payload)
      applyState(res.data)
    } catch (err: any) {
      if (err?.response?.status === 401) {
        clearStoredSession()
        await seed(true)
      }
      lastError.value = 'Failed to save data to backend'
      console.error(lastError.value, err)
    }
  }

  return {
    state,
    initialized,
    loading,
    lastError,
    applyState,
    seed,
    save,
  }
})
