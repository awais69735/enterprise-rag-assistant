from pathlib import Path

import pandas as pd

HR_FILE= Path("data/hr/hr_data.csv")

HR_FIELD_ACCESS = {
    "hr": {
        "employee_id",
        "full_name",
        "role",
        "department",
        "email",
        "location",
        "date_of_joining",
        "manager_id",
        "salary",
        "leave_balance",
        "leaves_taken",
        "attendance_pct",
        "performance_rating",
        "last_review_date",
    },
    "executive": {
        "employee_id",
        "full_name",
        "role",
        "department",
        "location",
        "date_of_joining",
        "manager_id",
        "salary",
        "leave_balance",
        "leaves_taken",
        "attendance_pct",
        "performance_rating",
        "last_review_date",
    },
}

class HRDataAccess:
    def __init__(self):
        self.df=pd.read_csv(HR_FILE)

    def query(self, role:str, question:str):
        """
        Return HR data only for roles authorized to access it.
        """

        if role not in HR_FIELD_ACCESS:
            return []

        allowed_fields= HR_FIELD_ACCESS[role]


        records= self.df[
            list(allowed_fields)
        ].to_dict(orient="records")

        return records

    def employee_count(self, role:str) -> int:
        if role not in HR_FIELD_ACCESS:
            return 0

        return int(self.df["employee_id"].nunique())

    def employee_by_joining_year(self, role:str) -> dict:
        if role not in HR_FIELD_ACCESS:
            return {}

        dates = pd.to_datetime(
            self.df["date_of_joining"],
            errors="coerce"
        )

        counts =(
            dates.dt.year
            .value_counts()
            .sort_index()
            .to_dict()
        )

        return {
            int(year): int(count)
            for year,count in counts.items()
        }

    def employee_by_department(self, role:str) -> dict:
        if role not in HR_FIELD_ACCESS:
            return {}

        counts = (
            self.df["department"]
            .value_counts()
            .sort_index()
            .to_dict()
        )

        return {
            str(department): int(count)
            for department, count in counts.items()
        }