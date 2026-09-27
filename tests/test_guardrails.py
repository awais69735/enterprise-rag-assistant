from app.guardrails.manager import GuardrailManager

guardrails= GuardrailManager()

def test_valid_question():
    result=guardrails.validate_question(
        "What are the company's financial results?"
    )

    assert result["allowed"] is True
    assert result["reason"] is None


def test_out_of_scope_question():
    result= guardrails.validate_question(
        "What is the weather today>"
    )
    assert result["allowed"] is False
    assert result["reason"] == "out_of_scope"

def test_email_pii():
    result= guardrails.validate_question(
        "What is john@example.com?"
    )

    assert result["allowed"] is False
    assert result["reason"] == "pii_detected"
    assert "email" in result["details"]

def test_phone_pii():
    result= guardrails.validate_question(
        "Call this number 123-456-7890."
    )

    assert result["allowed"] is False
    assert result["reason"] == "pii_detected"
    assert "phone" in result["details"]


def test_response_pii():
    result=guardrails.validate_response(
        "The employee email is john@example.com."
    )

    assert result["allowed"] is False
    assert result["reason"] == "pii_detected_in_response"
    assert "email" in result["details"]

def test_safe_response():
    result = guardrails.validate_response(
        "The company revenue increased during the reporting period."
    )

    assert result["allowed"] is True
    assert result["reason"] is None