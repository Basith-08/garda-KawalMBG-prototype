import unittest

from risk_assessment import build_distribution_assessment, normalize_distribution_record


class RiskAssessmentTest(unittest.TestCase):
    def test_high_risk_uses_weighted_operational_components(self):
        assessment = build_distribution_assessment(
            {
                "menuName": "Opor Ayam",
                "menuUtama": "Ayam opor santan",
                "schoolName": "SDN Uji",
                "durasi": 135,
                "suhu": 34,
                "catatan": "terlambat dan kemasan rusak",
                "vendorTrustScore": 42,
                "arrivalStatus": "received_with_issue",
                "qcPhotoUploaded": False,
                "packagingPhotoUploaded": False,
            }
        )

        self.assertEqual(assessment["riskStatus"], "HIGH")
        self.assertGreaterEqual(assessment["finalRiskScore"], 70)
        self.assertIn("soft block", assessment["recommendedAction"].lower())
        self.assertEqual(assessment["componentScores"]["arrivalVerificationRisk"], 70)

    def test_ok_arrival_and_complete_evidence_reduce_risk(self):
        assessment = build_distribution_assessment(
            {
                "menuName": "Nasi Tempe",
                "menuUtama": "Nasi, tempe orek, sayur",
                "schoolName": "SDN Uji",
                "durasi": 30,
                "suhu": 27,
                "arrivalStatus": "received_ok",
                "vendorTrustScore": 91,
                "qcPhotoUploaded": True,
                "packagingPhotoUploaded": True,
            }
        )

        self.assertEqual(assessment["riskStatus"], "LOW")
        self.assertLess(assessment["finalRiskScore"], 40)
        self.assertEqual(assessment["componentScores"]["sopRisk"], 0)

    def test_normalize_distribution_preserves_schema_fields_only_in_record(self):
        normalized = normalize_distribution_record(
            {
                "id": "risk-test",
                "vendorId": "1",
                "schoolName": "SDN Uji",
                "porsi": 100,
                "status": "safe",
                "statusText": "Safe",
                "time": "14 Mei 2026",
                "riskScore": 5,
                "menuName": "Opor Ayam",
                "menuUtama": "Ayam opor",
                "suhu": 34,
                "durasi": 120,
                "levelRisiko": "LOW",
                "catatan": "terlambat",
                "vendorTrustScore": 45,
            }
        )

        self.assertEqual(normalized["riskScore"], normalized["assessment"]["finalRiskScore"])
        self.assertIn(normalized["status"], {"safe", "medium", "high-risk"})


if __name__ == "__main__":
    unittest.main()
