from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.routes.upload import get_dataframe
from app.agents.planner_agent import PlannerAgent
from app.agents.data_agent import DataAgent
from app.agents.viz_agent import VizAgent
from app.agents.narrator_agent import NarratorAgent

router = APIRouter()

class QueryRequest(BaseModel):
    session_id: str
    question: str

@router.post("/ask")
async def ask_question(req: QueryRequest):
    """Multi-agent endpoint: plan -> execute -> visualize -> narrate."""
    df = get_dataframe(req.session_id)

    # Agent 1: Planner
    planner = PlannerAgent()
    plan = planner.plan(df, req.question)

    # Agent 2: Data execution
    data_agent = DataAgent()
    result = data_agent.execute(df, plan)

    # Agent 3: Visualization spec
    viz_agent = VizAgent()
    chart_spec = viz_agent.get_chart_spec(result, plan)

    # Agent 4: Narrator (uses OpenAI)
    narrator = NarratorAgent()
    narrative = narrator.narrate(req.question, result, plan)

    return {
        "question": req.question,
        "plan": plan,
        "result": result,
        "chart_spec": chart_spec,
        "narrative": narrative,
    }

@router.post("/report")
async def generate_report(req: QueryRequest):
    """Generate a downloadable Markdown report."""
    from app.analytics.query_executor import generate_markdown_report
    df = get_dataframe(req.session_id)
    report_md = generate_markdown_report(df, req.question)
    return {"report": report_md}
