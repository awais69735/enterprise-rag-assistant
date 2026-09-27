from app.rag.retriever import EnterpriseRetriever


def main():
    retriever = EnterpriseRetriever()

    question = "What are the company's financial results?"

    for role in ["finance", "marketing", "employee", "executive"]:
        print()
        print("=" * 80)
        print(f"ROLE: {role}")
        print("=" * 80)

        results = retriever.search(
            question=question,
            role=role,
            limit=5,
        )

        for result in results:
            payload = result.payload

            print(
                f"- {payload.get('source')} "
                f"| department={payload.get('department')} "
                f"| score={result.score:.4f}"
            )


if __name__ == "__main__":
    main()