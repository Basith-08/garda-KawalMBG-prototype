import { http } from './http'
import type { DistributionReceipt, ReceiptArrivalStatus, ReceiptIssueType } from '@/types/domain'

export interface ReceiptVerificationPayload {
  arrivalStatus: ReceiptArrivalStatus
  issueType?: ReceiptIssueType | null
  evidenceUploaded?: boolean
  note?: string
}

export async function fetchDistributionReceipt(distributionId: string) {
  const res = await http.get<DistributionReceipt>(`/api/distributions/${distributionId}/receipt`)
  return res.data
}

export async function submitDistributionReceipt(distributionId: string, payload: ReceiptVerificationPayload) {
  const res = await http.post<DistributionReceipt>(`/api/distributions/${distributionId}/receipt`, payload)
  return res.data
}
