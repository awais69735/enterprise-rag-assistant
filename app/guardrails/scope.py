ALLOWED_TOPICS ={
    "finance",
    "financial",
    "marketing",
    "sales",
    "hr",
    "employee",
    "engineering",
    "company",
    "business",
    "operations",
    "policy",
    "policies",
    "payroll",
    "leave",
    "attendance",
    "performance",
    "revenue",
    "expenses",
    "report",
    "reports"
}


def is_in_scope(question:str) -> bool:
    question_lower = question.lower()

    return any(
        topic in question_lower
        for topic in ALLOWED_TOPICS
    )