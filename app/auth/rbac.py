ROLE_ACCESS = {
    "finance": ["finance", "general"],
    "hr": ["hr", "general"],
    "marketing": ["marketing", "general"],
    "engineering": ["engineering", "general"],
    "executive": [
        "finance",
        "hr",
        "marketing",
        "engineering",
        "general",
    ],
    "employee": ["general"],
}


def get_allowed_departments(role: str) -> list[str]:
    return ROLE_ACCESS.get(role, [])