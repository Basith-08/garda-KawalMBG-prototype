import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/layouts/PublicLayout.vue'),
      children: [
        { path: '', name: 'landing', component: () => import('@/views/public/LandingPage.vue') },
        { path: 'vendor-score', name: 'vendor-score', component: () => import('@/views/public/VendorScorePage.vue') },
        { path: 'vendor-score/:id', name: 'vendor-score-detail', component: () => import('@/views/public/VendorScoreDetailPage.vue') },
        { path: 'education', name: 'education', component: () => import('@/views/public/EducationPage.vue') },
      ],
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/auth/LoginPage.vue'),
    },
    {
      path: '/regulator',
      component: () => import('@/layouts/DashboardLayout.vue'),
      meta: { requiresAuth: true, role: 'regulator' },
      children: [
        { path: '', redirect: '/regulator/dashboard' },
        { path: 'dashboard', name: 'regulator-dashboard', component: () => import('@/views/regulator/DashboardPage.vue') },
        { path: 'vendors', name: 'regulator-vendors', component: () => import('@/views/regulator/ListVendorPage.vue') },
        { path: 'vendors/:id', name: 'regulator-vendor-detail', component: () => import('@/views/regulator/VendorDetailPage.vue') },
        { path: 'vendors/:id/distribution/:distId', name: 'regulator-distribution-detail', component: () => import('@/views/regulator/DistributionDetailPage.vue') },
        { path: 'alerts', name: 'regulator-alerts', component: () => import('@/views/regulator/AlertsPage.vue') },
        { path: 'reports', name: 'regulator-reports', component: () => import('@/views/regulator/GenerateLaporanPage.vue') },
      ],
    },
    {
      path: '/vendor',
      component: () => import('@/layouts/DashboardLayout.vue'),
      meta: { requiresAuth: true, role: 'vendor' },
      children: [
        { path: '', redirect: '/vendor/dashboard' },
        { path: 'dashboard', name: 'vendor-dashboard', component: () => import('@/views/vendor/DashboardPage.vue') },
        { path: 'dashboard/history/:id', name: 'vendor-dashboard-history-detail', component: () => import('@/views/vendor/HistoryDetailPage.vue') },
        { path: 'input-distribusi', name: 'vendor-input-distribusi', component: () => import('@/views/vendor/InputDistribusiPage.vue') },
        { path: 'input-distribusi/result', name: 'vendor-input-distribusi-result', component: () => import('@/views/vendor/InputDistribusiResultPage.vue') },
        { path: 'history', name: 'vendor-history', component: () => import('@/views/vendor/HistoryPage.vue') },
        { path: 'history/:id', name: 'vendor-history-detail', component: () => import('@/views/vendor/HistoryDetailPage.vue') },
        { path: 'documents', name: 'vendor-documents', component: () => import('@/views/vendor/DokumenIzinPage.vue') },
      ],
    },
  ],
})

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' })
  } else if (to.meta.role && authStore.user?.role !== to.meta.role) {
    next({ name: 'login' })
  } else {
    next()
  }
})

export default router
