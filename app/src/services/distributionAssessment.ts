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
  ]
    .filter(Boolean)
    .join(' ')
    .toLowerCase()
}

function temperatureScore(temperature: number) {
  if (temperature >= 35) return { score: 34, reason: `Ambient temperature reached ${temperature.toFixed(0)}°C, accelerating unsafe exposure.` }
  if (temperature >= 32) return { score: 26, reason: `Ambient temperature remained elevated at ${temperature.toFixed(0)}°C.` }
  if (temperature >= 28) return { score: 16, reason: `Ambient temperature of ${temperature.toFixed(0)}°C increased exposure pressure.` }
  if (temperature >= 24) return { score: 8, reason: `Ambient temperature of ${temperature.toFixed(0)}°C stayed within monitored range.` }
  return { score: 4, reason: `Ambient temperature of ${temperature.toFixed(0)}°C stayed below the primary danger acceleration band.` }
}

function durationScore(duration: number) {
  if (duration > 120) return { score: 36, reason: `Distribution duration reached ${duration} minutes.` }
  if (duration > 90) return { score: 28, reason: `Distribution duration reached ${duration} minutes.` }
  if (duration > 60) return { score: 22, reason: `Distribution duration reached ${duration} minutes.` }
  if (duration > 45) return { score: 16, reason: `Distribution duration reached ${duration} minutes.` }
  if (duration > 30) return { score: 10, reason: `Distribution duration reached ${duration} minutes.` }
  return { score: 5, reason: `Distribution duration remained at ${duration} minutes.` }
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

  const temp = temperatureScore(temperature)
  const time = durationScore(duration)
  let score = 6 + temp.score + time.score
  riskFactors.push(temp.reason, time.reason)

  if (hasKeyword(combinedText, HIGH_PROTEIN_KEYWORDS)) {
    score += 16
    riskFactors.push('High-protein menu composition increased spoilage sensitivity.')
  }

  if (hasKeyword(combinedText, HIGH_MOISTURE_KEYWORDS)) {
    score += 10
    riskFactors.push('High-moisture menu components increased operational degradation sensitivity.')
  }

  if (duration > 45) {
    sopViolations.push('Route duration exceeded the 45-minute operational delivery threshold.')
  }

  if (temperature >= 32) {
    sopViolations.push('Ambient temperature entered the elevated exposure band at or above 32°C.')
  }

  if (hasKeyword(combinedText, ANOMALY_KEYWORDS)) {
    score += 24
    sopViolations.push('Operational anomaly signal detected in the field log.')
    riskFactors.push('Anomaly or discrepancy note increased operational uncertainty.')
  }

  if (hasKeyword(combinedText, DELAY_KEYWORDS)) {
    score += 10
    sopViolations.push('Delay-related signal detected in the operational note.')
    riskFactors.push('Delay signal increased cumulative exposure duration.')
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
    finalRiskScore,
    riskStatus,
    recommendedAction:
      riskStatus === 'HIGH'
        ? 'Escalate for immediate inspection and consumption control. Discard if additional holding continues.'
        : riskStatus === 'MEDIUM'
          ? 'Prioritize immediate handoff at destination and avoid additional non-refrigerated holding beyond 30 minutes.'
          : 'Maintain dispatch timing and continue routine operational monitoring.',
  }
}
