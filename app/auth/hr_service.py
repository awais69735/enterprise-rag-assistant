from app.auth.hr_router import HRIntentRouter
from app.auth.hr_tools import HRAnalysticsTool


class HRService:
    def __init__(self):
        self.router= HRIntentRouter()
        self .tools= HRAnalysticsTool()


    def process(self, question:str, role: str):
        intent= self.router.classify(question)

        if intent.intent== "employee_count":
            return self.tools.employee_count(role)

        if intent.intent== "employee_joining_trend":
            return self.tools.employee_joining_trend(role)

        if intent.intent == "employee_count_by_department":
            return self.tools.employee_count_by_department(role)

        return {
            "allowed":True,
            "operation": "unknown",
            "result":"None"
        }