import { http } from './http'

export interface AdminPlatformMetrics {
  totalUsers: number
  activeUsers: number
  superAdmins: number
  regulators: number
  vendors: number
  schools: number
  distributions: number
  highRiskDistributions: number
  alerts: number
  criticalAlerts: number
  expiringDocuments30d: number
}

export interface AdminDataQualityItem {
  code: string
  severity: 'high' | 'medium' | 'low'
  count: number
  description: string
}

export interface AdminUserAccessItem {
  id: string
  name: string
  email: string
  role: 'super-admin' | 'regulator' | 'vendor'
  vendorId?: string | null
  vendorName?: string | null
  isActive: boolean
  createdAt?: string | null
  lastLoginAt?: string | null
  avatar: string
}

export interface AdminVendorAttentionItem {
  id: string
  name: string
  status: string
  trustScore: number
  schoolCount: number
  distributionCount: number
  alertCount: number
  expiringDocumentCount: number
}

export interface AdminExpiringDocumentItem {
  id: string
  vendorId: string
  name: string
  expiry: string
  status: string
  daysLeft: number | null
}

export interface AdminOverview {
  platformMetrics: AdminPlatformMetrics
  dataQuality: AdminDataQualityItem[]
  userAccess: AdminUserAccessItem[]
  availableVendors: Array<{ id: string; name: string }>
  vendorAttention: AdminVendorAttentionItem[]
  expiringDocuments: AdminExpiringDocumentItem[]
}

export async function fetchAdminOverview() {
  const res = await http.get<AdminOverview>('/api/admin/overview')
  return res.data
}

export interface AdminUserUpdatePayload {
  role?: 'super-admin' | 'regulator' | 'vendor'
  vendorId?: string | null
  isActive?: boolean
}

export async function updateAdminUser(userId: string, payload: AdminUserUpdatePayload) {
  const res = await http.patch<AdminUserAccessItem>(`/api/admin/users/${userId}`, payload)
  return res.data
}
