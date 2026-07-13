from ai_output_eval.cli import evaluate_case


def test_evaluate_case_passes_clean_case():
    result = evaluate_case(
        {
            "case_id": "case-001",
            "output": {"invoice_id": "INV-001", "total": "1200"},
            "expected": {"invoice_id": "INV-001", "total": "1200"},
            "evidence": ["INV-001", "1200"],
            "confidence": {"invoice_id": 0.98, "total": 0.96},
        }
    )

    assert result["schema_valid"] is True
    assert result["field_accuracy"] == 1.0
    assert result["unsupported_claims"] == []
    assert result["posture_labels"]["rigor"] == "pass"
    assert result["posture_labels"]["caution"] == "pass"


def test_evaluate_case_flags_unsupported_claim_and_low_confidence():
    result = evaluate_case(
        {
            "case_id": "case-002",
            "output": {"invoice_id": "INV-002", "total": "1900", "issuer": "ACME"},
            "expected": {"invoice_id": "INV-002", "total": "1800"},
            "evidence": ["INV-002", "1800"],
            "confidence": {"invoice_id": 0.97, "total": 0.58, "issuer": 0.42},
        }
    )

    assert result["field_accuracy"] == 0.5
    assert "total=1900" in result["unsupported_claims"]
    assert "issuer=ACME" in result["unsupported_claims"]
    assert result["low_confidence_fields"] == ["total", "issuer"]
    assert result["posture_labels"]["rigor"] == "fail"
    assert result["posture_labels"]["candor"] == "warn"

