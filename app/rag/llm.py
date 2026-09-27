import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class RAGLLM:
    def __init__(self):
        api_key= os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        self.llm =ChatGroq(
            model="openai/gpt-oss-20b",
            temperature=0,
            api_key=api_key
        )

    def generate(
            self,
            question:str,
            context:str
    ) -> str:
        prompt =f"""
You are an internal enterprise assistant.

Answer the user's question using ONLY the provided context.

if the answer cannot be found in the context,
say:
"I don't have enough information in the available
company documents to answer that."

Do not invent facts.
Do not outside knowledge.

COMPANY CONTEXT:
{context}

USER QUESTION:
{question}

Answer:

"""
        response= self.llm.invoke(prompt)

        return response.content
