"""Unit tests for UI components (charts and tables).

Verifies that table formatters and Plotly chart generators produce correct
data structures, handle edge cases (e.g. empty results), and don't raise errors.
"""

import sys
import pandas as pd
import plotly.graph_objects as go
import pytest

sys.path.insert(0, r"c:\Users\adity\Desktop\ca-cse316")

from algorithms.fcfs import fcfs
from algorithms.scan import scan
from core.simulator import DiskSchedulerSimulator
from core.metrics import get_step_by_step_table, get_all_metrics
from components.tables import (
    format_step_by_step_table,
    format_comparison_table,
    format_metrics_summary,
)
from components.charts import (
    create_head_movement_chart,
    create_comparison_bar_chart,
    create_multi_head_movement_chart,
)


class TestTableFormatting:
    """Tests for components.tables module."""

    def test_format_step_by_step_table_normal(self):
        result = fcfs([98, 183, 37], 53)
        raw_steps = get_step_by_step_table(result)
        df = format_step_by_step_table(raw_steps)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert list(df.columns) == [
            "Step",
            "From Cylinder",
            "To Cylinder",
            "Head Movement",
            "Cumulative Movement",
        ]
        assert df.iloc[0]["Step"] == 1
        assert df.iloc[0]["From Cylinder"] == 53
        assert df.iloc[0]["To Cylinder"] == 98
        assert df.iloc[0]["Head Movement"] == 45
        assert df.iloc[0]["Cumulative Movement"] == 45

    def test_format_step_by_step_table_empty(self):
        df = format_step_by_step_table([])
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0
        assert "Step" in df.columns

    def test_format_comparison_table_normal(self):
        sim = DiskSchedulerSimulator([98, 183], 53)
        comp_data = sim.get_comparison_data()
        df = format_comparison_table(comp_data)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 4
        assert "Algorithm" in df.columns
        assert "Total Head Movement" in df.columns
        assert "Throughput (req/ms)" in df.columns

    def test_format_comparison_table_empty(self):
        df = format_comparison_table([])
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0

    def test_format_metrics_summary(self):
        result = scan([98, 183, 37], 53, direction="left")
        metrics = get_all_metrics(result, 0.1)
        df = format_metrics_summary(metrics, result)

        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["Metric", "Value"]
        metric_names = df["Metric"].tolist()
        assert "Algorithm Name" in metric_names
        assert "Total Head Movement" in metric_names
        assert "Initial Direction" in metric_names


class TestChartGeneration:
    """Tests for components.charts module."""

    def test_create_head_movement_chart_normal(self):
        result = scan([98, 183, 37], 53, direction="left")
        fig = create_head_movement_chart(result, min_cylinder=0, max_cylinder=199)

        assert isinstance(fig, go.Figure)
        assert len(fig.data) >= 1
        assert fig.data[0].name == "SCAN"
        assert list(fig.data[0].x) == result.head_movement_path

    def test_create_head_movement_chart_empty(self):
        result = fcfs([], 53)
        fig = create_head_movement_chart(result, min_cylinder=0, max_cylinder=199)

        assert isinstance(fig, go.Figure)

    def test_create_comparison_bar_chart(self):
        sim = DiskSchedulerSimulator([98, 183, 37], 53)
        comp_data = sim.get_comparison_data()
        fig = create_comparison_bar_chart(comp_data, metric="total_head_movement")

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1
        assert len(fig.data[0].x) == 4

    def test_create_multi_head_movement_chart(self):
        sim = DiskSchedulerSimulator([98, 183, 37], 53)
        all_results = sim.run_all_algorithms()
        fig = create_multi_head_movement_chart(all_results, min_cylinder=0, max_cylinder=199)

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 4
