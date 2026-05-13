import { http } from './http'

export interface RegulatorOverviewMetrics {
  vendors: number
  schools: number
  distributions: number
  highRiskDistributions: number
  activeAlerts: number
  delayedDistributions: number
  receiptIssues: number
  onTimeRate: number
}

export interface RegulatorTopVendorItem {
  id: string
  name: string
  trustScore: number
  status: 'safe' | 'medium' | 'high-risk'
  statusText: string
}

export interface RegulatorHighRiskItem {
  id: string
  vendorId: string
  vendorName: string
  schoolName: string
  riskScore: number
  statusText: string
  time: string
}

export interface RegulatorOverview {
  platformMetrics: RegulatorOverviewMetrics
  topVendors: RegulatorTopVendorItem[]
  recentHighRisk: RegulatorHighRiskItem[]
}

export async function fetchRegulatorOverview() {
  const res = await http.get<RegulatorOverview>('/api/regulator/overview')
  return res.data
}
