import type { Distribution, DistributionAssessment } from './api'

const HIGH_PROTEIN_KEYWORDS = [
  'ayam',
  'ikan',
  'daging',
  'rendang',
  'opor',
  'bakso',
  'sarden',
  'kambing',
  'telur',
  'geprek',
  'teri',
]

const HIGH_MOISTURE_KEYWORDS = [
  'soto',
  'rawon',
  'gulai',
  'kuah',
  'sayur',
  'opor',
  'tim',
  'gudeg',
  'asem',
  'bening',
  'sambal',
]

const ANOMALY_KEYWORDS = ['fraud', 'anomali', 'selisih', 'tidak sesuai', 'hilang', 'duplikasi']
const DELAY_KEYWORDS = ['terlambat', 'delay', 'lambat', 'pending', 'melebihi', 'telat']
const ISSUE_KEYWORDS = ['bau', 'tidak layak', 'kemasan rusak', 'rusak', 'jumlah kurang', 'porsi kurang', 'tidak sesuai', 'penyok', 'masalah']
const OK_KEYWORDS = ['diterima baik', 'konfirmasi positif', 'received ok', 'ok', 'lancar', 'no issues', 'safe']

function hasKeyword(text: string, keywords: string[]) {
  return keywords.some(keyword => text.includes(keyword))
}

function clamp(value: number, lower: number, upper: number) {
  return Math.max(lower, Math.min(upper, value))
}

function buildText(distribution: Partial<Distribution>) {
  return [
    distribution.menuName,
    distribution.menuUtama,
    distribution.statusText,
    distribution.catatan,
    distribution.status,
    distribution.vendorStatusText,
    distribution.arrivalVerification,
    distribution.arrivalStatus,
  ]
    .filter(Boolean)
    .join(' ')
    .toLowerCase()
}

function timeRisk(duration: number) {
  if (duration <= 0) return { score: 100, reason: 'Time risk: production-to-arrival timeline is incomplete.' }
  if (duration <= 45) return { score: 10, reason: `Time risk: route duration stayed within the 45-minute dispatch target (${duration} minutes).` }
  if (duration <= 60) return { score: 40, reason: `Time risk: route duration exceeded the 45-minute dispatch target (${duration} minutes).` }
  if (duration <= 120) return { score: 70, reason: `Time risk: route duration created extended distribution exposure (${duration} minutes).` }
  return { score: 90, reason: `Time risk: route duration exceeded 2 hours (${duration} minutes).` }
}

function sopRisk(distribution: Partial<Distribution>, combinedText: string) {
  const evidenceFields = [
    'qcPhotoUploaded',
    'productionPhotoUploaded',
    'packagingPhotoUploaded',
    'vehiclePhotoUploaded',
    'evidenceUploaded',
  ] as const
  const presentFields = evidenceFields.filter(field => field in distribution)
  const uploadedCount = presentFields.filter(field => Boolean(distribution[field])).length

  if (presentFields.length > 0) {
    const missing = presentFields.length - uploadedCount
    if (missing === 0) return { score: 0, reason: 'SOP risk: required QC and dispatch evidence is complete.' }
    if (missing === 1) return { score: 40, reason: 'SOP risk: one required evidence item is missing.' }
    if (missing === 2) return { score: 70, reason: 'SOP risk: multiple evidence items are missing.' }
    return { score: 100, reason: 'SOP risk: required operational evidence was not uploaded.' }
  }

  if (hasKeyword(combinedText, ANOMALY_KEYWORDS)) return { score: 85, reason: 'SOP risk: discrepancy or anomaly signal was detected in the operational log.' }
  if (hasKeyword(combinedText, DELAY_KEYWORDS)) return { score: 60, reason: 'SOP risk: delay signal was detected in the operational log.' }
  return { score: 40, reason: 'SOP risk: evidence completeness is not available in the current distribution record.' }
}

function menuRisk(combinedText: string) {
  const highProtein = hasKeyword(combinedText, HIGH_PROTEIN_KEYWORDS)
  const highMoisture = hasKeyword(combinedText, HIGH_MOISTURE_KEYWORDS)
  if (highProtein && highMoisture) return { score: 70, reason: 'Menu risk: high-protein and high-moisture components increase food sensitivity.' }
  if (highProtein) return { score: 50, reason: 'Menu risk: high-protein menu composition requires tighter exposure control.' }
  if (highMoisture) return { score: 50, reason: 'Menu risk: high-moisture menu components require tighter exposure control.' }
  return { score: 20, reason: 'Menu risk: menu composition is relatively stable for distribution.' }
}

function arrivalRisk(distribution: Partial<Distribution>, combinedText: string) {
  const rawStatus = String(distribution.arrivalVerification || distribution.arrivalStatus || '').trim().toLowerCase()
  if (['ok', 'received_ok', 'received-good', 'received_good', 'diterima_baik'].includes(rawStatus)) {
    return { score: 0, reason: 'Arrival verification risk: school confirmed receipt without issue.' }
  }
  if (['not_confirmed', 'unconfirmed', 'belum_dikonfirmasi'].includes(rawStatus)) {
    return { score: 50, reason: 'Arrival verification risk: school receipt is not yet confirmed.' }
  }
  if (['issue', 'received_with_issue', 'problem', 'ada_masalah'].includes(rawStatus)) {
    return { score: 70, reason: 'Arrival verification risk: school reported an issue on receipt.' }
  }
  if (['major_issue', 'rejected', 'heavy_issue'].includes(rawStatus)) {
    return { score: 100, reason: 'Arrival verification risk: school reported a severe receipt issue.' }
  }

  if (hasKeyword(combinedText, ISSUE_KEYWORDS)) return { score: 70, reason: 'Arrival verification risk: field note indicates a receipt or quality issue.' }
  if (hasKeyword(combinedText, OK_KEYWORDS)) return { score: 0, reason: 'Arrival verification risk: field note indicates normal receipt.' }
  return { score: 50, reason: 'Arrival verification risk: school receipt is not yet confirmed.' }
}

function vendorHistoryRisk(distribution: Partial<Distribution>, combinedText: string) {
  if (distribution.vendorTrustScore !== undefined) {
    const trust = distribution.vendorTrustScore
    if (trust >= 85) return { score: 0, reason: `Vendor history risk: vendor trust score is strong (${trust.toFixed(0)}).` }
    if (trust >= 70) return { score: 30, reason: `Vendor history risk: vendor trust score needs monitoring (${trust.toFixed(0)}).` }
    if (trust >= 50) return { score: 70, reason: `Vendor history risk: vendor trust score is weak (${trust.toFixed(0)}).` }
    return { score: 100, reason: `Vendor history risk: vendor trust score is critical (${trust.toFixed(0)}).` }
  }

  if (hasKeyword(combinedText, ['investigasi', 'critical', 'fraud', 'high risk incident'])) {
    return { score: 100, reason: 'Vendor history risk: active investigation or critical history signal detected.' }
  }
  if (hasKeyword(combinedText, ['sering', 'laporan buruk', 'high-risk'])) {
    return { score: 70, reason: 'Vendor history risk: repeated negative history signal detected.' }
  }
  if (hasKeyword(combinedText, DELAY_KEYWORDS)) return { score: 30, reason: 'Vendor history risk: prior delay signal detected.' }
  return { score: 0, reason: 'Vendor history risk: no negative history signal was available.' }
}

function weatherRisk(temperature: number) {
  if (temperature >= 35) return { score: 80, reason: `Weather risk: ambient temperature reached ${temperature.toFixed(0)}°C.` }
  if (temperature >= 32) return { score: 60, reason: `Weather risk: ambient temperature remained elevated at ${temperature.toFixed(0)}°C.` }
  if (temperature >= 28) return { score: 35, reason: `Weather risk: ambient temperature of ${temperature.toFixed(0)}°C adds moderate context.` }
  return { score: 10, reason: `Weather risk: ambient temperature of ${temperature.toFixed(0)}°C adds limited context.` }
}

function estimateDangerZoneMinutes(duration: number, temperature: number) {
  if (temperature >= 32) return duration
  if (temperature >= 28) return Math.max(10, Math.round(duration * 0.8))
  if (temperature >= 24) return Math.max(5, Math.round(duration * 0.55))
  return Math.max(0, Math.round(duration * 0.25))
}

export function statusFromRisk(riskStatus: DistributionAssessment['riskStatus']): Distribution['status'] {
  if (riskStatus === 'HIGH') return 'high-risk'
  if (riskStatus === 'MEDIUM') return 'medium'
  return 'safe'
}

export function assessDistribution(distribution: Partial<Distribution>): DistributionAssessment {
  const menuName = distribution.menuName ?? 'Unknown Menu'
  const schoolName = distribution.schoolName ?? 'Unknown Destination'
  const duration = distribution.durasi ?? 0
  const temperature = distribution.suhu ?? 0
  const combinedText = buildText(distribution)
  const riskFactors: string[] = []
  const sopViolations: string[] = []

  const time = timeRisk(duration)
  const sop = sopRisk(distribution, combinedText)
  const menu = menuRisk(combinedText)
  const arrival = arrivalRisk(distribution, combinedText)
  const vendorHistory = vendorHistoryRisk(distribution, combinedText)
  const weather = weatherRisk(temperature)
  const score =
    time.score * 0.25 +
    sop.score * 0.25 +
    menu.score * 0.15 +
    arrival.score * 0.20 +
    vendorHistory.score * 0.10 +
    weather.score * 0.05
  riskFactors.push(time.reason, sop.reason, menu.reason, arrival.reason, vendorHistory.reason, weather.reason)

  if (duration > 45) {
    sopViolations.push('Route duration exceeded the 45-minute operational delivery threshold.')
  }

  if (sop.score >= 70) sopViolations.push(sop.reason)
  if (arrival.score >= 70) sopViolations.push(arrival.reason)

  if (hasKeyword(combinedText, ANOMALY_KEYWORDS)) {
    sopViolations.push('Operational anomaly signal detected in the field log.')
  }

  if (hasKeyword(combinedText, DELAY_KEYWORDS)) {
    sopViolations.push('Delay-related signal detected in the operational note.')
  }

  const finalRiskScore = Math.round(clamp(score, 5, 98))
  const riskStatus: DistributionAssessment['riskStatus'] =
    finalRiskScore >= 70 ? 'HIGH' : finalRiskScore >= 40 ? 'MEDIUM' : 'LOW'

  if (sopViolations.length === 0) {
    sopViolations.push('No major SOP violation was detected from the available delivery log.')
  }

  return {
    operationalSummary: `${menuName} for ${schoolName} shows ${riskStatus.toLowerCase()} operational exposure driven by ${duration} minutes of distribution time and ambient temperature of ${temperature.toFixed(0)}°C.`,
    exposureAnalysis: [
      `Total exposure duration: ${duration} minutes`,
      `Estimated danger-zone exposure: ${estimateDangerZoneMinutes(duration, temperature)} minutes`,
      `Ambient temperature: ${temperature.toFixed(0)}°C`,
      'Holding condition: no refrigerated evidence in the current delivery log',
    ],
    sopViolations,
    riskFactors,
    componentScores: {
      timeRisk: time.score,
      sopRisk: sop.score,
      menuRisk: menu.score,
      arrivalVerificationRisk: arrival.score,
      vendorHistoryRisk: vendorHistory.score,
      weatherRisk: weather.score,
    },
    finalRiskScore,
    riskStatus,
    recommendedAction:
      riskStatus === 'HIGH'
        ? 'Apply soft block pending supervisor approval, require additional evidence, and alert the regulator dashboard.'
        : riskStatus === 'MEDIUM'
          ? 'Allow distribution with QC evidence requirement and mandatory school receipt monitoring.'
          : 'Allow normal distribution and keep the operational log for audit.',
  }
}
