from app.auth.hr_router import HRIntentRouter


def main():

    router = HRIntentRouter()

    questions = [
        "How many employees do we have?",
        "What's our current headcount?",
        "How large is our workforce?",
        "Show me how our workforce grew over the years.",
        "How many people joined the company each year?",
        "Give me the employee breakdown by department.",
        "How many people work in Finance?",
        "Tell me about the company cafeteria.",
    ]

    for question in questions:

        result = router.classify(question)

        print()
        print("=" * 80)
        print(f"QUESTION: {question}")
        print("=" * 80)
        print(f"INTENT: {result.intent}")


if __name__ == "__main__":
    main()