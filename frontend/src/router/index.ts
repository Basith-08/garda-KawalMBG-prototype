import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/layouts/PublicLayout.vue'),
      children: [
        { path: '', name: 'landing', component: () => import('@/pages/public/LandingPage.vue') },
        { path: 'vendor-score', name: 'vendor-score', component: () => import('@/pages/public/VendorScorePage.vue') },
        { path: 'vendor-score/:id', name: 'vendor-score-detail', component: () => import('@/pages/public/VendorScoreDetailPage.vue') },
        { path: 'education', name: 'education', component: () => import('@/pages/public/EducationPage.vue') },
        { path: 'receipt/:id', name: 'receipt', component: () => import('@/pages/public/ReceiptPage.vue') },
      ],
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/pages/auth/LoginPage.vue'),
    },
    {
      path: '/regulator',
      component: () => import('@/layouts/DashboardLayout.vue'),
      meta: { requiresAuth: true, role: 'regulator' },
      children: [
        { path: '', redirect: '/regulator/dashboard' },
        { path: 'dashboard', name: 'regulator-dashboard', component: () => import('@/pages/regulator/DashboardPage.vue') },
        { path: 'vendors', name: 'regulator-vendors', component: () => import('@/pages/regulator/ListVendorPage.vue') },
        { path: 'vendors/:id', name: 'regulator-vendor-detail', component: () => import('@/pages/regulator/VendorDetailPage.vue') },
        { path: 'vendors/:id/distribution/:distId', name: 'regulator-distribution-detail', component: () => import('@/pages/regulator/DistributionDetailPage.vue') },
        { path: 'alerts', name: 'regulator-alerts', component: () => import('@/pages/regulator/AlertsPage.vue') },
        { path: 'reports', name: 'regulator-reports', component: () => import('@/pages/regulator/GenerateLaporanPage.vue') },
      ],
    },
    {
      path: '/super-admin',
      component: () => import('@/layouts/DashboardLayout.vue'),
      meta: { requiresAuth: true, role: 'super-admin' },
      children: [
        { path: '', redirect: '/super-admin/dashboard' },
        { path: 'dashboard', name: 'super-admin-dashboard', component: () => import('@/pages/admin/SuperAdminDashboardPage.vue') },
      ],
    },
    {
      path: '/vendor',
      component: () => import('@/layouts/DashboardLayout.vue'),
      meta: { requiresAuth: true, role: 'vendor' },
      children: [
        { path: '', redirect: '/vendor/dashboard' },
        { path: 'dashboard', name: 'vendor-dashboard', component: () => import('@/pages/vendor/DashboardPage.vue') },
        { path: 'dashboard/history/:id', name: 'vendor-dashboard-history-detail', component: () => import('@/pages/vendor/HistoryDetailPage.vue') },
        { path: 'input-distribusi', name: 'vendor-input-distribusi', component: () => import('@/pages/vendor/InputDistribusiPage.vue') },
        { path: 'input-distribusi/result', name: 'vendor-input-distribusi-result', component: () => import('@/pages/vendor/InputDistribusiResultPage.vue') },
        { path: 'history', name: 'vendor-history', component: () => import('@/pages/vendor/HistoryPage.vue') },
        { path: 'history/:id', name: 'vendor-history-detail', component: () => import('@/pages/vendor/HistoryDetailPage.vue') },
        { path: 'documents', name: 'vendor-documents', component: () => import('@/pages/vendor/DokumenIzinPage.vue') },
      ],
    },
  ],
})

router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !(await authStore.restoreSession())) {
    next({ name: 'login' })
  } else if (to.meta.role && authStore.user?.role !== to.meta.role) {
    next({ name: 'login' })
  } else {
    next()
  }
})

export default router
