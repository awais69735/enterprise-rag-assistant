from app.rag.retriever import EnterpriseRetriever
from app.rag.llm import RAGLLM

class RAGPipeline:
    def __init__(self):
        self.retriever = EnterpriseRetriever()
        self.llm = RAGLLM()

    def answer(
            self,
            question:str,
            role:str,
            top_k:int=5
    ):
        results= self.retriever.search(
            question,
            role=role,
            limit=top_k
        )

        context_parts= []

        sources= []

        for result in results:

            payload = result.payload
            text = payload.get("text","")
            context_parts.append(text)
            sources.append(
                {
                    "source": payload.get("source"),
                    "department":payload.get("department"),
                    "score": result.score
                }
            )

        context= "\n\n".join(context_parts)

        if not context:
            return {
                "answer":(
                    "I don't have access to information"
                    "that can answer this question."
                ),
                "sources":[]
            }

        answer = self.llm.generate(
            question=question,
            context=context
        )

        return {
            "answer":answer,
            "sources":sources
        }
