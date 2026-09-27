import re
from app.auth.hr_access import HRDataAccess

class HRQueryService:

    def __init__(self):
        self.hr = HRDataAccess()

    def can_handle(self, question:str) -> bool:
        question_lower = question.lower()

        keywords= [
            "employee count",
            "how many employees",
            "number of employees",
            "employee do we have",
            "employee report",
            "employee joined",
            "joined each year",
            "joining year",
            "employees by year",
            "employees per year",
            "employee by department"
        ]
        return any(
            keywords in question_lower
            for keyword in keywords
        )

    def answer(self, question:str, role:str):
        if role not in {"hr","executive"}:
            return {
                "handled":True,
                "allowed": False,
                "answer":(
                    "You do not have permission to access"
                    "employee information"
                ),
                "data": None
            }

        question_lower = question.lower()

        if (
            "how many employees" in question_lower
            or "employee count" in question_lower
            or "number of employees" in question_lower
            or "employees do we have" in question_lower
        ):
            count = self.hr.employee_count(role)

            return {
                "handled": True,
                "allowed": True,
                "answer":(
                    f"This company has {count} employees."
                ),
                "data":
            }