import json
from pathlib import Path


from qdrant_client import QdrantClient
from qdrant_client.models import Distance,VectorParams, PointStruct
from sentence_transformers import SentenceTransformer


# ----------------
# Configuration
# -----------------


INPUT_FILE= Path(
    "processed_data/document_chunks.json"
)

COLLECTION_NAME= "star_charts"

QDRANT_URL= "http://localhost:6333"

EMBEDDING_MODEL= "BAAI/bge-small-en-v1.5"


# --------------------------------
# Load Chunks
# --------------------------


def load_chunks():
    with INPUT_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


# ------------------------
# Main
# --------------------


def main():
    print("Loading document chunks ...")
    chunks= load_chunks()

    print(f"Loaded {len(chunks)} chunks.")


    # ------------------------
    # Load Embedding Model
    # ------------------------

    print()
    print("Loading embedding model ...")

    model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    print("Embedding Model Loaded.")

    # ---------
    # Create Qdrant client
    # --------------------

    client = QdrantClient(
        url=QDRANT_URL
    )

    test_embedding= model.encode(
        "test sentence"
    )

    vector_size= len(test_embedding)

    print(
        f"Embedding Dimension: {vector_size}"
    )

    # ----------------------
    # Recreate collection
    # ----------------------

    if client.collection_exists(
        COLLECTION_NAME
    ):
        print(
            f"Deleting existing collection: "
            f"{COLLECTION_NAME}"
        )

        client.delete_collection(
            COLLECTION_NAME
        )

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=vector_size,
            distance= Distance.COSINE
        )
    )

    print(
        f"Created Collection: "
        f"{COLLECTION_NAME}"
    )

    # ----------------------------
    # Create Embeddings
    # --------------------------


    texts= [
        chunk["text"]
        for chunk in chunks
    ]

    print()
    print("Creating embeddings...")

    embeddings= model.encode(
        texts,
        show_progress_bar=True
    )

    print("Embedding Created")

    # ---------------------
    # Create Qdrant points
    # ----------------------

    points= []

    for index, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):
        points.append(
            PointStruct(
                id=index,
                vector= embedding.tolist(),

                payload={
                    "text": chunk["text"],
                    **chunk["metadata"]
                }
            )
        )

    # --------------------------
    # Upload
    # --------------------------

    print()
    print("Uploading vectors to Qdrant...")

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print()
    print("Vector Database setup complete.")


    # -----------------------
    # Collection information
    # -----------------------

    collection_info= client.get_collection(
        COLLECTION_NAME
    )

    print()
    print(
        f"Vectors stored: "
        f"{collection_info.points_count}"
    )


if __name__== "__main__":
    main()
