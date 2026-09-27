from app.auth.hr_tools import HRAnalysticsTool

def main():
    tool= HRAnalysticsTool()

    print("="*80)
    print("EMPLOYEE COUNT")
    print("="*80)

    print(
        tool.employee_count("hr")
    )

    print()
    print("="*80)
    print("JOINING TREND")
    print("="*80)

    print(
        tool.employee_joining_trend("hr")
    )

    print()
    print("="*80)
    print("DEPARTMENT COUNT")
    print("="*80)

    print(
        tool.employee_count_by_department("hr")
    )


    print()
    print("="*80)
    print("UNAUTHORIZED ACCESS")
    print("="*80)

    print(
        tool.employee_count("finance")
    )

if __name__=="__main__":
    main()