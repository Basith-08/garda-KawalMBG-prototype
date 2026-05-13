export interface Vendor {
  id: string
  name: string
  status: 'safe' | 'medium' | 'high-risk'
  statusText: string
  trustScore: number
  trustBreakdown?: {
    timeliness: number
    evidence: number
    schoolReceipt: number
    portionConsistency: number
    history: number
  } | null
  trend: number
  trendDir: 'up' | 'down'
  address: string
  joinDate: string
  schools: string[]
}

export interface School {
  id: string
  name: string
  npsn: string
  address: string
  vendorId: string
  vendorName: string
  trustScore: number
  status: 'safe' | 'medium' | 'high-risk'
  statusText: string
}

export type ReceiptArrivalStatus = 'received_ok' | 'received_with_issue' | 'not_received' | 'not_confirmed'
export type ReceiptIssueType =
  | 'packaging_damaged'
  | 'portion_shortage'
  | 'unsafe_smell_or_quality'
  | 'menu_mismatch'
  | 'late_arrival'
  | 'not_received'
  | 'other'

export interface DistributionAssessment {
  operationalSummary: string
  exposureAnalysis: string[]
  sopViolations: string[]
  riskFactors: string[]
  componentScores?: {
    timeRisk: number
    sopRisk: number
    menuRisk: number
    arrivalVerificationRisk: number
    vendorHistoryRisk: number
    weatherRisk: number
  }
  finalRiskScore: number
  riskStatus: 'LOW' | 'MEDIUM' | 'HIGH'
  recommendedAction: string
}

export interface Distribution {
  id: string
  vendorId: string
  schoolName: string
  porsi: number
  status: 'safe' | 'medium' | 'high-risk'
  statusText: string
  time: string
  riskScore: number
  menuName: string
  menuUtama: string
  suhu: number
  durasi: number
  levelRisiko: string
  catatan: string
  cookedAt?: string
  packagedAt?: string
  pickupAt?: string
  deliveredAt?: string
  vendorTrustScore?: number
  vendorStatusText?: string
  arrivalVerification?: string
  arrivalStatus?: ReceiptArrivalStatus
  receiptIssueType?: ReceiptIssueType | null
  receiptEvidenceUploaded?: boolean
  receiptNote?: string | null
  receiptVerifiedAt?: string | null
  qcPhotoUploaded?: boolean
  productionPhotoUploaded?: boolean
  packagingPhotoUploaded?: boolean
  vehiclePhotoUploaded?: boolean
  evidenceUploaded?: boolean
  assessment?: DistributionAssessment
}

export interface DistributionReceipt {
  id: string
  vendorId: string
  schoolName: string
  menuName: string
  menuUtama: string
  porsi: number
  time: string
  arrivalStatus?: ReceiptArrivalStatus
  receiptIssueType?: ReceiptIssueType | null
  receiptEvidenceUploaded?: boolean
  receiptNote?: string | null
  receiptVerifiedAt?: string | null
  assessment: DistributionAssessment
}

export interface Alert {
  id: string
  type: 'CRITICAL' | 'FRAUD'
  vendorId?: string
  vendorName: string
  description: string
  time: string
  statusTag: string
}

export interface Document {
  id: string
  vendorId: string
  name: string
  expiry: string
  status: 'Valid' | 'Expired'
}
