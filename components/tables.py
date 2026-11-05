"""Table formatting utilities for the disk scheduling simulator.

This module formats raw simulation data and performance metrics into clean,
human-readable pandas DataFrames suitable for presentation in Streamlit.
"""

from typing import Any
import pandas as pd
from algorithms.common import SchedulingResult


def format_step_by_step_table(step_data: list[dict[str, Any]]) -> pd.DataFrame:
    """Format step-by-step head movement data into a display DataFrame.

    Args:
        step_data: List of dicts produced by core.metrics.get_step_by_step_table.
            Each dict has keys: 'step', 'previous_head', 'current_request',
            'movement', 'cumulative_movement'.

    Returns:
        pd.DataFrame: A formatted DataFrame with column headers:
            'Step', 'From Cylinder', 'To Cylinder', 'Head Movement', 'Cumulative Movement'.
    """
    columns = [
        "Step",
        "From Cylinder",
        "To Cylinder",
        "Head Movement",
        "Cumulative Movement",
    ]

    if not step_data:
        return pd.DataFrame(columns=columns)

    rows = []
    for item in step_data:
        rows.append(
            {
                "Step": item.get("step", 0),
                "From Cylinder": item.get("previous_head", 0),
                "To Cylinder": item.get("current_request", 0),
                "Head Movement": item.get("movement", 0),
                "Cumulative Movement": item.get("cumulative_movement", 0),
            }
        )

    return pd.DataFrame(rows, columns=columns)


def format_comparison_table(comparison_data: list[dict[str, Any]]) -> pd.DataFrame:
    """Format multi-algorithm comparison data into a display DataFrame.

    Args:
        comparison_data: List of dicts produced by
            core.simulator.DiskSchedulerSimulator.get_comparison_data.
            Each dict contains 'algorithm', 'total_head_movement',
            'average_head_movement', 'total_seek_time', 'average_seek_time',
            'throughput'.

    Returns:
        pd.DataFrame: A formatted DataFrame with rounded numeric values.
    """
    columns = [
        "Algorithm",
        "Total Head Movement",
        "Avg Head Movement",
        "Total Seek Time (ms)",
        "Avg Seek Time (ms)",
        "Throughput (req/ms)",
    ]

    if not comparison_data:
        return pd.DataFrame(columns=columns)

    rows = []
    for item in comparison_data:
        throughput_val = item.get("throughput", 0.0)
        throughput_str = "∞" if throughput_val == float("inf") else f"{throughput_val:.4f}"

        rows.append(
            {
                "Algorithm": item.get("algorithm", "Unknown"),
                "Total Head Movement": int(item.get("total_head_movement", 0)),
                "Avg Head Movement": round(float(item.get("average_head_movement", 0.0)), 2),
                "Total Seek Time (ms)": round(float(item.get("total_seek_time", 0.0)), 2),
                "Avg Seek Time (ms)": round(float(item.get("average_seek_time", 0.0)), 2),
                "Throughput (req/ms)": throughput_str,
            }
        )

    df = pd.DataFrame(rows, columns=columns)
    return df


def format_metrics_summary(metrics: dict[str, Any], result: SchedulingResult) -> pd.DataFrame:
    """Create a key-value metric summary table for a single algorithm result.

    Args:
        metrics: Dictionary returned by core.metrics.get_all_metrics.
        result: SchedulingResult instance.

    Returns:
        pd.DataFrame: Two-column DataFrame with 'Metric' and 'Value'.
    """
    throughput_val = metrics.get("throughput", 0.0)
    throughput_str = "∞" if throughput_val == float("inf") else f"{throughput_val:.4f} req/ms"

    data = [
        {"Metric": "Algorithm Name", "Value": result.algorithm_name},
        {"Metric": "Total Requests Serviced", "Value": str(len(result.request_sequence))},
        {"Metric": "Initial Head Position", "Value": str(result.head_movement_path[0]) if result.head_movement_path else "N/A"},
        {"Metric": "Total Head Movement", "Value": f"{metrics.get('total_head_movement', 0)} cylinders"},
        {"Metric": "Average Head Movement", "Value": f"{metrics.get('average_head_movement', 0.0):.2f} cylinders/req"},
        {"Metric": "Total Seek Time", "Value": f"{metrics.get('total_seek_time', 0.0):.2f} ms"},
        {"Metric": "Average Seek Time", "Value": f"{metrics.get('average_seek_time', 0.0):.2f} ms/req"},
        {"Metric": "Throughput", "Value": throughput_str},
    ]

    if result.direction is not None:
        data.append({"Metric": "Initial Direction", "Value": result.direction.capitalize()})

    return pd.DataFrame(data)

