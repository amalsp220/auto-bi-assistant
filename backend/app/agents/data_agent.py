import pandas as pd
from app.analytics.query_executor import safe_execute_code

class DataAgent:
    """
    Data Agent: Executes pandas code plans using only OSS libraries.
    No paid APIs involved - pure Python execution.
    """

    def execute(self, df: pd.DataFrame, plan: dict) -> dict:
        code = plan.get("pandas_code", "result = df.describe()")
        result = safe_execute_code(df, code)
        result["code_executed"] = code
        return result
