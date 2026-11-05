"""Plotly visualization components for disk scheduling algorithms.

This module provides functions to create interactive Plotly visualizations
of disk head traversal paths and algorithm performance comparisons.
"""

from typing import Any
import plotly.graph_objects as go
from algorithms.common import SchedulingResult

# Palette for consistent algorithm branding
ALGORITHM_COLORS = {
    "FCFS": "#3b82f6",   # Blue
    "SSTF": "#10b981",   # Emerald green
    "SCAN": "#f59e0b",   # Amber
    "C-SCAN": "#8b5cf6", # Purple
}


def create_head_movement_chart(
    result: SchedulingResult,
    min_cylinder: int = 0,
    max_cylinder: int = 199,
    title: str | None = None,
) -> go.Figure:
    """Create a Plotly figure showing the disk head traversal path.

    Renders the classic textbook representation of disk scheduling:
    - X-axis: Cylinder Number (min_cylinder to max_cylinder)
    - Y-axis: Traversal Step (Step 0 at top, increasing downwards)

    Args:
        result: The SchedulingResult containing the head_movement_path.
        min_cylinder: Minimum cylinder number for the disk range.
        max_cylinder: Maximum cylinder number for the disk range.
        title: Optional custom chart title.

    Returns:
        go.Figure: An interactive Plotly figure.
    """
    path = result.head_movement_path
    if not path:
        fig = go.Figure()
        fig.update_layout(
            title=title or f"{result.algorithm_name or 'Algorithm'} — Head Movement",
            annotations=[
                {
                    "text": "No head movement to display (empty request sequence).",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 16},
                }
            ],
            xaxis={"range": [min_cylinder, max_cylinder]},
            yaxis={"autorange": "reversed"},
            template="plotly_white",
        )
        return fig

    steps = list(range(len(path)))
    algo_color = ALGORITHM_COLORS.get(result.algorithm_name.upper(), "#2563eb")

    # Movements per step for hover tooltip
    # Step 0 is starting point (0 movement)
    movements = [0] + result.individual_movements
    while len(movements) < len(path):
        movements.append(0)

    # Marker colors: highlight start (green) and end (red)
    marker_colors = []
    marker_symbols = []
    for i, cyl in enumerate(path):
        if i == 0:
            marker_colors.append("#22c55e")  # Start: Green
            marker_symbols.append("circle")
        elif i == len(path) - 1:
            marker_colors.append("#ef4444")  # End: Red
            marker_symbols.append("square")
        elif cyl in (min_cylinder, max_cylinder) and result.algorithm_name.upper() in ("SCAN", "C-SCAN"):
            marker_colors.append("#f97316")  # Boundary: Orange
            marker_symbols.append("diamond")
        else:
            marker_colors.append(algo_color)
            marker_symbols.append("circle")

    fig = go.Figure()

    # Main path trace
    fig.add_trace(
        go.Scatter(
            x=path,
            y=steps,
            mode="lines+markers+text",
            line=dict(color=algo_color, width=2.5, dash="solid"),
            marker=dict(
                size=11,
                color=marker_colors,
                symbol=marker_symbols,
                line=dict(color="#ffffff", width=1.5),
            ),
            text=[str(cyl) for cyl in path],
            textposition="top right",
            customdata=movements,
            hovertemplate=(
                "<b>Step %{y}</b><br>"
                "Cylinder: <b>%{x}</b><br>"
                "Seek from previous: %{customdata} cyl<extra></extra>"
            ),
            name=result.algorithm_name,
        )
    )

    chart_title = title or f"{result.algorithm_name} — Disk Head Movement Trajectory"

    fig.update_layout(
        title=dict(text=chart_title, font=dict(size=18, family="Arial, sans-serif")),
        xaxis=dict(
            title="Cylinder Number",
            range=[min_cylinder - 2, max_cylinder + 2],
            tickmode="auto",
            nticks=15,
            showgrid=True,
            gridcolor="#e2e8f0",
            zeroline=False,
        ),
        yaxis=dict(
            title="Movement Step Sequence (Top to Bottom)",
            autorange="reversed",
            tickmode="linear",
            tick0=0,
            dtick=1,
            showgrid=True,
            gridcolor="#f1f5f9",
        ),
        template="plotly_white",
        hovermode="closest",
        margin=dict(l=60, r=40, t=60, b=60),
        height=520,
    )

    return fig


def create_comparison_bar_chart(
    comparison_data: list[dict[str, Any]],
    metric: str = "total_head_movement",
    title: str | None = None,
) -> go.Figure:
    """Create a bar chart comparing all algorithms on a specific metric.

    Args:
        comparison_data: List of dicts produced by
            core.simulator.DiskSchedulerSimulator.get_comparison_data.
        metric: Metric key to plot ('total_head_movement', 'average_seek_time',
            'throughput', etc.). Defaults to 'total_head_movement'.
        title: Optional custom chart title.

    Returns:
        go.Figure: An interactive Plotly bar chart.
    """
    metric_labels = {
        "total_head_movement": ("Total Head Movement (Cylinders)", "cylinders"),
        "average_head_movement": ("Average Head Movement (Cylinders/Request)", "cyl/req"),
        "total_seek_time": ("Total Seek Time (ms)", "ms"),
        "average_seek_time": ("Average Seek Time (ms/Request)", "ms"),
        "throughput": ("Throughput (Requests/ms)", "req/ms"),
    }

    y_axis_label, unit = metric_labels.get(
        metric, (metric.replace("_", " ").title(), "")
    )

    algorithms = [d.get("algorithm", "Unknown") for d in comparison_data]
    raw_values = [d.get(metric, 0) for d in comparison_data]

    # Handle infinite throughput gracefully in chart
    values = []
    text_labels = []
    for v in raw_values:
        if v == float("inf"):
            values.append(0)
            text_labels.append("∞")
        elif isinstance(v, float):
            values.append(v)
            text_labels.append(f"{v:.2f}")
        else:
            values.append(v)
            text_labels.append(str(v))

    colors = [
        ALGORITHM_COLORS.get(algo.upper(), "#3b82f6") for algo in algorithms
    ]

    fig = go.Figure(
        data=[
            go.Bar(
                x=algorithms,
                y=values,
                text=text_labels,
                textposition="outside",
                marker=dict(
                    color=colors,
                    line=dict(color="#1e293b", width=1),
                ),
                hovertemplate="<b>%{x}</b><br>" + y_axis_label + ": %{text}<extra></extra>",
            )
        ]
    )

    chart_title = title or f"Algorithm Comparison — {y_axis_label}"

    fig.update_layout(
        title=dict(text=chart_title, font=dict(size=18, family="Arial, sans-serif")),
        xaxis=dict(title="Algorithm", tickfont=dict(size=13, weight="bold")),
        yaxis=dict(
            title=y_axis_label,
            showgrid=True,
            gridcolor="#e2e8f0",
        ),
        template="plotly_white",
        margin=dict(l=60, r=40, t=60, b=50),
        height=450,
    )

    return fig


def create_multi_head_movement_chart(
    results: dict[str, SchedulingResult],
    min_cylinder: int = 0,
    max_cylinder: int = 199,
    title: str | None = None,
) -> go.Figure:
    """Create an overlay plot displaying all algorithm trajectories on one chart.

    Args:
        results: Dictionary mapping algorithm names to their SchedulingResult.
        min_cylinder: Minimum disk cylinder.
        max_cylinder: Maximum disk cylinder.
        title: Optional custom title.

    Returns:
        go.Figure: Interactive multi-trace Plotly figure.
    """
    fig = go.Figure()

    dash_styles = {
        "fcfs": "solid",
        "sstf": "dash",
        "scan": "dot",
        "cscan": "dashdot",
    }

    for key, result in results.items():
        path = result.head_movement_path
        if not path:
            continue
        steps = list(range(len(path)))
        name = result.algorithm_name or key.upper()
        color = ALGORITHM_COLORS.get(name.upper(), "#3b82f6")
        dash = dash_styles.get(key.lower(), "solid")

        fig.add_trace(
            go.Scatter(
                x=path,
                y=steps,
                mode="lines+markers",
                name=f"{name} ({result.total_head_movement} cyl)",
                line=dict(color=color, width=2.5, dash=dash),
                marker=dict(size=7),
                hovertemplate=(
                    f"<b>{name}</b><br>"
                    "Step %{y}: Cylinder <b>%{x}</b><extra></extra>"
                ),
            )
        )

    fig.update_layout(
        title=dict(
            text=title or "Head Movement Comparison — All Algorithms Overlay",
            font=dict(size=18, family="Arial, sans-serif"),
        ),
        xaxis=dict(
            title="Cylinder Number",
            range=[min_cylinder - 2, max_cylinder + 2],
            showgrid=True,
            gridcolor="#e2e8f0",
        ),
        yaxis=dict(
            title="Movement Step",
            autorange="reversed",
            showgrid=True,
            gridcolor="#f1f5f9",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        template="plotly_white",
        hovermode="closest",
        margin=dict(l=60, r=40, t=80, b=50),
        height=540,
    )

    return fig
