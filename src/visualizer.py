"""
Visualizer — Plotly charts for skill match breakdown.
"""

import plotly.graph_objects as go
from typing import Dict


def plot_skill_match(gaps: Dict) -> go.Figure:
    """Bar chart showing matched vs missing vs extra skills."""
    categories = ["Matched ✅", "Missing ❌", "Extra 🔵"]
    values = [
        len(gaps["matched_skills"]),
        len(gaps["missing_skills"]),
        len(gaps["extra_skills"]),
    ]
    colors = ["#00f5a0", "#ff6b6b", "#00d4ff"]

    fig = go.Figure(go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        text=values,
        textposition="outside",
        textfont=dict(color="white", size=14, family="Syne"),
    ))

    fig.update_layout(
        title=dict(
            text="Skill Distribution",
            font=dict(family="Syne", size=16, color="#e8eaf0"),
        ),
        paper_bgcolor="#0b0c10",
        plot_bgcolor="#13141a",
        font=dict(family="DM Mono", color="#6b7280"),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color="#e8eaf0", size=12),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#1e2030",
            tickfont=dict(color="#6b7280"),
        ),
        margin=dict(t=50, b=30, l=30, r=30),
        height=300,
    )
    return fig


def plot_score_gauge(score: int) -> go.Figure:
    """Gauge chart for overall match score."""
    color = "#00f5a0" if score >= 70 else "#ffd166" if score >= 45 else "#ff6b6b"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Match Score", "font": {"family": "Syne", "color": "#e8eaf0", "size": 14}},
        number={"suffix": "%", "font": {"family": "Syne", "color": color, "size": 36}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#6b7280", "tickwidth": 1},
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": "#13141a",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 45], "color": "rgba(255,107,107,0.1)"},
                {"range": [45, 70], "color": "rgba(255,209,102,0.1)"},
                {"range": [70, 100], "color": "rgba(0,245,160,0.1)"},
            ],
            "threshold": {
                "line": {"color": color, "width": 3},
                "thickness": 0.75,
                "value": score,
            },
        }
    ))

    fig.update_layout(
        paper_bgcolor="#0b0c10",
        margin=dict(t=30, b=20, l=20, r=20),
        height=220,
    )
    return fig
