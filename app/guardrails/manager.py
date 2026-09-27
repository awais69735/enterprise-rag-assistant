from app.guardrails.pii import detect_pii
from app.guardrails.scope import is_in_scope


class GuardrailManager:

    def validate_question(self, question:str) -> dict:
        pii_detected = detect_pii(question)

        if pii_detected:
            return {
                "allowed":False,
                "reason": "pii_detected",
                "details": pii_detected
            }

        if not is_in_scope(question):
            return {
                "allowed": False,
                "reason":"out_of_scope",
                "details": []
            }

        return {
            "allowed": True,
            "reason":None,
            "details": []
        }

    def validate_response(self, response:str) -> dict:
        pii_detected= detect_pii(response)

        if pii_detected:
            return {
                "allowed": False,
                "reason": "pii_detected_in_response",
                "details": pii_detected
            }

        return {
            "allowed":True,
            "reason": None,
            "details": []
        }
