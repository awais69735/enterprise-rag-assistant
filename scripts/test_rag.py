from app.rag.pipeline import RAGPipeline


def main():
    rag = RAGPipeline()

    question = input("\nEnter your question: ")

    for role in ["finance", "employee", "executive"]:
        print()
        print("=" * 80)
        print(f"ROLE: {role}")
        print("=" * 80)

        result = rag.answer(
            question=question,
            role=role,
        )

        print()
        print("ANSWER")
        print("-" * 80)
        print(result["answer"])

        print()
        print("SOURCES")
        print("-" * 80)

        for source in result["sources"]:
            print(
                f"- {source['source']} "
                f"| {source['department']} "
                f"| score={source['score']:.4f}"
            )


if __name__ == "__main__":
    main()