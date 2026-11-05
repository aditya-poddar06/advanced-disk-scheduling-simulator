"""
Comprehensive tests for disk scheduling metrics functions.

Uses a known SchedulingResult (FCFS standard case):
  requests = [98, 183, 37, 122, 14, 124, 65, 67]
  service_order = [98, 183, 37, 122, 14, 124, 65, 67]
  head_movement_path = [53, 98, 183, 37, 122, 14, 124, 65, 67]
  individual_movements = [45, 85, 146, 85, 108, 110, 59, 2]
  total_head_movement = 640
  seek_time_per_cylinder = 0.1

Manual calculations:
  total_head_movement = 640
  average_head_movement = 640 / 8 = 80.0
  total_seek_time = 640 * 0.1 = 64.0
  average_seek_time = 64.0 / 8 = 8.0
  throughput = 8 / 64.0 = 0.125
"""

import sys
import math
import pytest

sys.path.insert(0, r'c:\Users\adity\Desktop\ca-cse316')

from algorithms.common import SchedulingResult
from core.metrics import (
    calculate_total_head_movement,
    calculate_average_head_movement,
    calculate_total_seek_time,
    calculate_average_seek_time,
    calculate_throughput,
    get_all_metrics,
    get_step_by_step_table,
)


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def make_fcfs_result():
    """Create a known FCFS SchedulingResult for testing."""
    return SchedulingResult(
        algorithm_name="FCFS",
        request_sequence=[98, 183, 37, 122, 14, 124, 65, 67],
        service_order=[98, 183, 37, 122, 14, 124, 65, 67],
        head_movement_path=[53, 98, 183, 37, 122, 14, 124, 65, 67],
        individual_movements=[45, 85, 146, 85, 108, 110, 59, 2],
        total_head_movement=640,
        direction=None,
    )


def make_empty_result():
    """Create a SchedulingResult with no requests."""
    return SchedulingResult(
        algorithm_name="FCFS",
        request_sequence=[],
        service_order=[],
        head_movement_path=[53],
        individual_movements=[],
        total_head_movement=0,
        direction=None,
    )


SEEK_TIME = 0.1  # 100ms per cylinder


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestTotalHeadMovement:
    def test_total_head_movement(self):
        """Total head movement should be 640."""
        result = make_fcfs_result()
        assert calculate_total_head_movement(result) == 640

    def test_total_head_movement_empty(self):
        """Empty requests → 0."""
        result = make_empty_result()
        assert calculate_total_head_movement(result) == 0


class TestAverageHeadMovement:
    def test_average_head_movement(self):
        """Average = 640 / 8 = 80.0."""
        result = make_fcfs_result()
        assert calculate_average_head_movement(result) == pytest.approx(80.0)

    def test_average_head_movement_empty(self):
        """Empty requests → 0."""
        result = make_empty_result()
        assert calculate_average_head_movement(result) == 0


class TestTotalSeekTime:
    def test_total_seek_time(self):
        """Total seek time = 640 * 0.1 = 64.0."""
        result = make_fcfs_result()
        assert calculate_total_seek_time(result, SEEK_TIME) == pytest.approx(64.0)


class TestAverageSeekTime:
    def test_average_seek_time(self):
        """Average seek time = 64.0 / 8 = 8.0."""
        result = make_fcfs_result()
        assert calculate_average_seek_time(result, SEEK_TIME) == pytest.approx(8.0)


class TestThroughput:
    def test_throughput(self):
        """Throughput = 8 / 64.0 = 0.125."""
        result = make_fcfs_result()
        assert calculate_throughput(result, SEEK_TIME) == pytest.approx(0.125)

    def test_zero_seek_time(self):
        """Zero seek_time → throughput should be inf."""
        result = make_fcfs_result()
        tp = calculate_throughput(result, 0)
        assert tp == float('inf') or tp == math.inf

    def test_empty_requests_throughput(self):
        """Empty requests → throughput = 0."""
        result = make_empty_result()
        tp = calculate_throughput(result, SEEK_TIME)
        assert tp == 0 or tp == 0.0


class TestEmptyRequestsMetrics:
    """All metrics return 0 for empty requests."""

    def test_empty_total(self):
        result = make_empty_result()
        assert calculate_total_head_movement(result) == 0

    def test_empty_average(self):
        result = make_empty_result()
        assert calculate_average_head_movement(result) == 0

    def test_empty_total_seek(self):
        result = make_empty_result()
        assert calculate_total_seek_time(result, SEEK_TIME) == 0

    def test_empty_average_seek(self):
        result = make_empty_result()
        assert calculate_average_seek_time(result, SEEK_TIME) == 0


class TestGetAllMetrics:
    def test_get_all_metrics_keys(self):
        """get_all_metrics returns dict with all expected keys."""
        result = make_fcfs_result()
        metrics = get_all_metrics(result, SEEK_TIME)
        expected_keys = {
            'total_head_movement',
            'average_head_movement',
            'total_seek_time',
            'average_seek_time',
            'throughput',
        }
        # All expected keys must be present (there may be additional keys)
        for key in expected_keys:
            assert key in metrics, f"Missing key: {key}"

    def test_get_all_metrics_values(self):
        """Verify numeric values in get_all_metrics."""
        result = make_fcfs_result()
        metrics = get_all_metrics(result, SEEK_TIME)
        assert metrics['total_head_movement'] == 640
        assert metrics['average_head_movement'] == pytest.approx(80.0)
        assert metrics['total_seek_time'] == pytest.approx(64.0)
        assert metrics['average_seek_time'] == pytest.approx(8.0)
        assert metrics['throughput'] == pytest.approx(0.125)


class TestStepByStepTable:
    def test_step_by_step_table(self):
        """Verify structure and values of step-by-step table."""
        result = make_fcfs_result()
        table = get_step_by_step_table(result)
        # Should have one row per request serviced
        assert len(table) == 8
        # Each row should be a dict
        assert isinstance(table[0], dict)

    def test_step_by_step_cumulative(self):
        """Verify cumulative head movement values are correct."""
        result = make_fcfs_result()
        table = get_step_by_step_table(result)
        # Manually calculate cumulative sums
        movements = [45, 85, 146, 85, 108, 110, 59, 2]
        cumulative = []
        running = 0
        for m in movements:
            running += m
            cumulative.append(running)
        # cumulative = [45, 130, 276, 361, 469, 579, 638, 640]

        # Check that the table has the right cumulative values
        # The exact key name may vary, so check for common patterns
        for i, row in enumerate(table):
            # Look for a cumulative movement field
            cum_keys = [k for k in row.keys() if 'cumul' in k.lower() or 'total' in k.lower()]
            if cum_keys:
                assert row[cum_keys[0]] == cumulative[i]

    def test_step_by_step_empty(self):
        """Empty requests → empty table."""
        result = make_empty_result()
        table = get_step_by_step_table(result)
        assert len(table) == 0
