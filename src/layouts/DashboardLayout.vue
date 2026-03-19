<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const role = computed(() => authStore.user?.role || 'vendor')
const isMobileMenuOpen = ref(false)

const regulatorMenu = [
  { label: 'Dashboard', to: '/regulator/dashboard', icon: 'pi pi-th-large' },
  { label: 'List Vendor', to: '/regulator/vendors', icon: 'pi pi-list' },
  { label: 'Alerts', to: '/regulator/alerts', icon: 'pi pi-bell' },
  { label: 'Generate Laporan', to: '/regulator/reports', icon: 'pi pi-file' },
]

const vendorMenu = [
  { label: 'Dashboard', to: '/vendor/dashboard', icon: 'pi pi-th-large' },
  { label: 'Input Distribusi', to: '/vendor/input-distribusi', icon: 'pi pi-pencil' },
  { label: 'Histori Distribusi', to: '/vendor/history', icon: 'pi pi-clock' },
  { label: 'Dokumen & Izin', to: '/vendor/documents', icon: 'pi pi-file' },
]

const menu = computed(() => role.value === 'regulator' ? regulatorMenu : vendorMenu)

function isActive(to: string) {
  return route.path.startsWith(to)
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="min-h-screen flex relative overflow-x-hidden">
    <!-- Mobile Menu Overlay -->
    <div 
      v-if="isMobileMenuOpen" 
      class="fixed inset-0 bg-black/50 z-40 md:hidden" 
      @click="isMobileMenuOpen = false"
    ></div>

    <!-- Sidebar -->
    <aside 
      class="w-[260px] bg-white border-r border-navy-200 flex flex-col shrink-0 fixed md:sticky top-0 h-screen z-50 transition-transform duration-300 ease-in-out md:translate-x-0"
      :class="isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <!-- Logo -->
      <div class="px-5 py-4 flex items-center gap-3 border-b border-navy-200">
        <div class="w-10 h-10 rounded-full bg-navy-900 flex items-center justify-center shrink-0">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M12 2L3 7v6c0 5.25 3.83 10.16 9 11.27 5.17-1.11 9-6.02 9-11.27V7l-9-5z" fill="#fff" opacity="0.3"/>
            <circle cx="12" cy="12" r="4" fill="#fff"/>
          </svg>
        </div>
        <span class="text-lg font-bold text-navy-900">KawalMBG</span>
      </div>

      <!-- Menu -->
      <nav class="flex-1 px-3 py-4 space-y-1">
        <router-link
          v-for="item in menu"
          :key="item.to"
          :to="item.to"
          class="flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200"
          :class="isActive(item.to) ? 'bg-navy-800 text-white shadow-sm' : 'text-navy-600 hover:bg-navy-100'"
          @click="isMobileMenuOpen = false"
        >
          <i :class="item.icon" class="text-base"></i>
          {{ item.label }}
        </router-link>
      </nav>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col min-h-screen w-full md:w-auto md:max-w-[calc(100vw-260px)]">
      <!-- Top Bar -->
      <header class="bg-navy-900 text-white px-4 md:px-6 py-3 flex items-center justify-between md:justify-end gap-4 sticky top-0 z-30 shadow-md md:shadow-none">
        <!-- Hamburger for Mobile -->
        <button class="md:hidden p-2 hover:bg-navy-800 rounded-lg transition-colors" @click="isMobileMenuOpen = true">
          <i class="pi pi-bars text-xl"></i>
        </button>

        <!-- Right Tools -->
        <div class="flex items-center gap-4">
          <button class="relative p-2 hover:bg-navy-800 rounded-lg transition-colors">
            <i class="pi pi-bell text-lg"></i>
            <span class="absolute -top-0.5 -right-0.5 w-5 h-5 bg-brand-danger text-white text-[10px] font-bold rounded-full flex items-center justify-center">9</span>
          </button>
          <div class="flex items-center gap-3 cursor-pointer" @click="handleLogout">
            <img :src="authStore.user?.avatar" class="w-9 h-9 rounded-full object-cover border-2 border-navy-600" alt="avatar" />
            <div class="text-right hidden sm:block">
              <div class="text-sm font-semibold leading-tight">{{ authStore.user?.name }}</div>
              <div class="text-xs capitalize" :class="role === 'regulator' ? 'text-brand-danger' : 'text-brand-success'">{{ role }}</div>
            </div>
            <i class="pi pi-chevron-down text-xs text-navy-400 hidden sm:block"></i>
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <main class="flex-1 p-4 md:p-6 bg-navy-50 overflow-y-auto overflow-x-hidden relative">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>
