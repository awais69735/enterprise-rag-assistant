from typing import Literal

from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os


load_dotenv()


class HRIntent(BaseModel):
    intent: Literal[
        "employee_count",
        "employee_joining_trend",
        "employee_count_by_department",
        "unknown"
    ] =Field(
        description="The HR operation required to answer the user's question."
    )

class HRIntentRouter:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        self.llm = ChatGroq(
            model="openai/gpt-oss-20b",
            temperature=0,
            api_key=api_key
        )

        self.router = self.llm.with_structured_output(
            HRIntent
        )

    def classify(self, question:str) -> HRIntent:

        prompt= f"""
You are an enterprise HR query router.

Determine which structured HR operation is needed to answer the user's question.

Avaliable operation:

1. employee_count
    Question asking about total employee/headcount.

2. employee_joining_trend
    Question asking about employees joining over time,
    yearly hiring, workforce growth by joining year,
    or employee counts by year.

3. employee_count_by_department
    Question asking about employees group by department.

4. unknown
    Question that canont be answer using htese HR operations.


Understand natural language and different writh styles.
Do not require the user to use specific keywords.

Examples: 

"How many employees do we have?"
->employee_count

"What's out current headcount?"
->employee_count

"How large is our workforce?"
->employee_count

"Show me how our workforce grew over the years."
→ employee_joining_trend

"How many people joined the company each year?"
→ employee_joining_trend

"Give me the employee breakdown by department."
→ employee_count_by_department

"How many people work in Finance?"
→ employee_count_by_department

Question:
{question}
"""
        return self.router.invoke(prompt)