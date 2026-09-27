from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

from app.auth.rbac import get_allowed_departments

QDRANT_URL="http://localhost:6333"
COLLECTION_NAME="star_charts"
EMBEDDING_MODEL="BAAI/bge-small-en-v1.5"


class EnterpriseRetriever:
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL)

        self.embedding_model = SentenceTransformer(
            EMBEDDING_MODEL
        )

    def search(
            self,
            question:str,
            role:str,
            limit:int=5
    ):
        allowed_departments= get_allowed_departments(role)


        if not allowed_departments:
            return []

        query_vector= self.embedding_model.encode(
            question
        ).tolist()

        results= self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            query_filter={
                "must": [
                    {
                        "key":"department",
                        "match":{
                            "any": allowed_departments
                        }
                    }
                ]
            },
            limit=limit
        )

        return results.points
