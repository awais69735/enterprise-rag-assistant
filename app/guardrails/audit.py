import json 
from datetime import datetime, timezone
from pathlib import Path


AUDIT_DIR =Path("logs")
AUDIT_FILE= AUDIT_DIR / "guardrail_audit.jsonl"


def log_guardrails_event(
        username:str,
        role:str,
        action:str,
        reason:str,
        details:list[str],
):
    AUDIT_DIR.mkdir(exist_ok=True)

    event= {
        "timstamp": datetime.now(timezone.utc).isoformat(),
        "username":username,
        "role":role,
        "action":action,
        "reason":reason,
        "details":details,

    }

    with AUDIT_FILE.open("a",encoding="utf-8") as file:
        file.write(json.dumps(event)+"\n")