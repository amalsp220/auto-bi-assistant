import pytest
import pandas as pd
from app.agents.data_agent import DataAgent
from app.agents.viz_agent import VizAgent

def test_data_agent_executes_valid_code():
    df = pd.DataFrame({"name": ["A", "B", "C"], "value": [10, 20, 30]})
    plan = {"pandas_code": "result = df['value'].sum()"}
    agent = DataAgent()
    result = agent.execute(df, plan)
    assert result["data"] == 60

def test_data_agent_handles_error():
    df = pd.DataFrame({"x": [1, 2, 3]})
    plan = {"pandas_code": "result = df['nonexistent']"}
    agent = DataAgent()
    result = agent.execute(df, plan)
    assert result["error"] is not None

def test_viz_agent_returns_bar_spec():
    result = {"data": [{"name": "A", "value": 10}, {"name": "B", "value": 20}]}
    plan = {"chart_type": "bar", "x_col": "name", "y_col": "value"}
    agent = VizAgent()
    spec = agent.get_chart_spec(result, plan)
    assert spec is not None
    assert spec["type"] == "bar"

def test_viz_agent_returns_none_for_error():
    result = {"error": "fail"}
    plan = {"chart_type": "bar"}
    agent = VizAgent()
    spec = agent.get_chart_spec(result, plan)
    assert spec is None
