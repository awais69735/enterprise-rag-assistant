from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


COLLECTION_NAME= "star_charts"

QDRANT_URL = "http://localhost:6333"

EMBEDDING_MODEL= "BAAI/bge-small-en-v1.5"


def main():
    client = QdrantClient(
        url=QDRANT_URL
    )

    model= SentenceTransformer(
        EMBEDDING_MODEL
    )

    question = input(
        "\n Enter your question: "
    )

    query_vector= model.encode(
        question
    ).tolist()

    results= client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=5
    )

    print()
    print("="*70)
    print("SEARCH RESULTS")
    print("="*70)

    for index, result in enumerate(
        results.points,
        start=1
    ):
        print()
        print(f"Result #{index}")
        print("-"*70)

        print(
            f"Score: {result.score:4f}"
        )

        print(
            f"Source: ",
            f"{result.payload.get("source")}"
        )

        print(
            f"Department: ",
            f"{result.payload.get("department")}"
        )
        
        print()
        print(
            result.payload.get("text")
        )

if __name__=="__main__":
    main()
