import json
from app.core.openai_client import client
from app.core.config import settings

class NarratorAgent:
    """
    Narrator Agent: Produces natural-language explanation using OpenAI.
    Only this agent uses the OpenAI API; everything else is OSS.
    """

    def narrate(self, question: str, result: dict, plan: dict) -> str:
        if result.get("error"):
            return f"The data query encountered an error: {result['error']}. Please try rephrasing your question."

        result_summary = json.dumps(result.get("data"), default=str)[:2000]
        explanation = plan.get("explanation", "")

        system_prompt = (
            "You are a data analyst communicator. Given a user's question, the analysis plan, "
            "and the computed result, write a clear, concise, insightful 2-4 sentence explanation. "
            "Mention specific numbers from the result. Be direct and informative."
        )

        user_prompt = (
            f"Question: {question}\n\n"
            f"Analysis approach: {explanation}\n\n"
            f"Computed result (JSON): {result_summary}"
        )

        try:
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=300,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Analysis complete. Result: {result_summary[:500]}"
