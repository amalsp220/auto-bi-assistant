from typing import Optional

CHART_TYPE_MAP = {
    "bar": {"label": "Bar Chart", "recharts": "BarChart"},
    "line": {"label": "Line Chart", "recharts": "LineChart"},
    "scatter": {"label": "Scatter Plot", "recharts": "ScatterChart"},
    "histogram": {"label": "Histogram", "recharts": "BarChart"},
    "pie": {"label": "Pie Chart", "recharts": "PieChart"},
    "none": {"label": "No Chart", "recharts": None},
}

class VizAgent:
    """
    Visualization Agent: Produces chart specs from execution results.
    Pure OSS logic - no paid APIs. Frontend renders with Recharts (OSS).
    """

    def get_chart_spec(self, result: dict, plan: dict) -> Optional[dict]:
        chart_type = plan.get("chart_type", "none")
        x_col = plan.get("x_col")
        y_col = plan.get("y_col")

        if chart_type == "none" or result.get("error"):
            return None

        data = result.get("data", [])
        if not data:
            return None

        # Normalize data for Recharts format
        if isinstance(data, dict):
            # Series data - convert to list of {name, value}
            chart_data = [{"name": str(k), "value": v} for k, v in data.items()]
            x_col = x_col or "name"
            y_col = y_col or "value"
        elif isinstance(data, list):
            chart_data = data
        else:
            return None

        return {
            "type": chart_type,
            "recharts_component": CHART_TYPE_MAP.get(chart_type, {}).get("recharts"),
            "label": CHART_TYPE_MAP.get(chart_type, {}).get("label", chart_type),
            "x_key": x_col,
            "y_key": y_col,
            "data": chart_data[:200],  # Cap at 200 points for performance
        }
