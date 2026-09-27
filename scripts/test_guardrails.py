from app.guardrails.manager import GuardrailManager


def main():
    guardrails= GuardrailManager()

    questions =[
        "What are the company's financial results?",
        "What is the marketing budet?",
        "What is the weather today?",
        "What is John's email john@email.com?",
        "Tell me about employee attendance."
    ]

    for question in questions:
        result = guardrails.validate_question(question)

        print()
        print("="*80)
        print(f"QUESTION: {question}")
        print("="*80)

        print(result)

        print()
        print("=" * 80)
        print("RESPONSE PII TEST")
        print("=" * 80)

        response = "The employee contact email is john@example.com."

        result = guardrails.validate_response(response)

        print(result)


if __name__=="__main__":
    main()