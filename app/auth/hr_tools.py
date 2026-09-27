from app.auth.hr_access import HRDataAccess

class HRAnalysticsTool:

    def __init__(self):
        self.hr = HRDataAccess()


    def employee_count(self, role:str) -> dict:
        if role not in {"hr", "executive"}:
            return {
                "allowed": False,
                "error": "Access Denied."
            }

        count = self.hr.employee_count(role)

        return {
            "allowed": True,
            "operation": "employee_count",
            "result": {
                "employee_count": count
            }
        }

    def employee_joining_trend(self, role:str)-> dict:
        if role not in {"hr","executive"}:
            return {
                "allowed":False,
                "error": "Access Denied"
            }

        result = self.hr.employee_by_joining_year(role)

        return {
            "allowed": True,
            "operation": "employee_joining_trend",
            "result": result
        }

    def employee_count_by_department(self, role:str) -> dict:
        if role not in {"hr", "executive"}:
            return {
                "allowed": False,
                "error": "Access denied."
            }

        result = self.hr.employee_by_department(role)

        return {
            "allowed": True,
            "operation": "employee_count_by_department",
            "result": result
        }