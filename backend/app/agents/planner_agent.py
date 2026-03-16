import json
import pandas as pd
from app.core.openai_client import client
from app.core.config import settings
from app.analytics.data_profiler import get_schema_summary

class PlannerAgent:
    """
    Planner Agent: Uses OpenAI to design a query execution plan.
    All orchestration logic is open-source; only the LLM call uses OpenAI.
    """

    def plan(self, df: pd.DataFrame, question: str) -> dict:
        schema = get_schema_summary(df)
        sample = df.head(settings.MAX_SAMPLE_ROWS).fillna("").to_csv(index=False)

        system_prompt = (
            "You are a data analyst planning agent. Given a dataset schema and a user question, "
            "produce a JSON execution plan with these fields:\n"
            "  - pandas_code: Python code using pandas (df variable is available) that computes the answer. "
            "    Store final result in variable named 'result'.\n"
            "  - chart_type: one of [bar, line, scatter, histogram, pie, none]\n"
            "  - x_col: column name for x-axis (or null)\n"
            "  - y_col: column name for y-axis (or null)\n"
            "  - explanation: brief plain-English explanation of the plan\n"
            "Return ONLY valid JSON. No markdown."
        )

        user_prompt = (
            f"Dataset schema:\n{schema}\n\n"
            f"Sample rows (CSV):\n{sample}\n\n"
            f"Question: {question}"
        )

        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
            max_tokens=800,
        )

        raw = response.choices[0].message.content.strip()
        try:
            plan = json.loads(raw)
        except json.JSONDecodeError:
            plan = {
                "pandas_code": "result = df.describe()",
                "chart_type": "none",
                "x_col": None,
                "y_col": None,
                "explanation": "Fallback plan: could not parse LLM response.",
                "raw_response": raw,
            }
        return plan
