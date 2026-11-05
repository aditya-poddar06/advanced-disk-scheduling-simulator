"""
Comprehensive tests for FCFS (First-Come, First-Served) disk scheduling algorithm.

Manual calculations for standard test case:
  requests = [98, 183, 37, 122, 14, 124, 65, 67], initial_head = 53, disk 0-199
  Path: 53 -> 98 -> 183 -> 37 -> 122 -> 14 -> 124 -> 65 -> 67
  Movements: |98-53|=45, |183-98|=85, |37-183|=146, |122-37|=85,
             |14-122|=108, |124-14|=110, |65-124|=59, |67-65|=2
  Total: 45+85+146+85+108+110+59+2 = 640
  Service order: [98, 183, 37, 122, 14, 124, 65, 67]  (same as input)
"""

import sys
import pytest

sys.path.insert(0, r'c:\Users\adity\Desktop\ca-cse316')

from algorithms.fcfs import fcfs


# ---------------------------------------------------------------------------
# Standard test data
# ---------------------------------------------------------------------------
REQUESTS = [98, 183, 37, 122, 14, 124, 65, 67]
INITIAL_HEAD = 53
MIN_CYL = 0
MAX_CYL = 199

EXPECTED_SERVICE_ORDER = [98, 183, 37, 122, 14, 124, 65, 67]
EXPECTED_PATH = [53, 98, 183, 37, 122, 14, 124, 65, 67]
EXPECTED_INDIVIDUAL_MOVEMENTS = [45, 85, 146, 85, 108, 110, 59, 2]
EXPECTED_TOTAL = 640


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestFCFSBasic:
    """Basic correctness tests with manually-calculated expected values."""

    def test_fcfs_basic(self):
        """Standard test: verify all result fields against manual calculation."""
        result = fcfs(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL)
        assert result.algorithm_name.lower().replace('-', '').replace('_', '').replace(' ', '') == "fcfs"
        assert result.request_sequence == REQUESTS
        assert result.service_order == EXPECTED_SERVICE_ORDER
        assert result.head_movement_path == EXPECTED_PATH
        assert result.individual_movements == EXPECTED_INDIVIDUAL_MOVEMENTS
        assert result.total_head_movement == EXPECTED_TOTAL

    def test_fcfs_service_order(self):
        """FCFS services requests in the exact order they arrive."""
        result = fcfs(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL)
        assert result.service_order == EXPECTED_SERVICE_ORDER
        # Service order must be identical to input request order for FCFS
        assert result.service_order == list(REQUESTS)

    def test_fcfs_total_movement(self):
        """Total head movement = 640 for the standard test case."""
        result = fcfs(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL)
        assert result.total_head_movement == 640

    def test_fcfs_individual_movements(self):
        """Each individual movement matches manual calculation."""
        result = fcfs(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL)
        assert result.individual_movements == [45, 85, 146, 85, 108, 110, 59, 2]
        # Verify sum equals total
        assert sum(result.individual_movements) == result.total_head_movement


class TestFCFSEdgeCases:
    """Edge-case tests."""

    def test_fcfs_empty_requests(self):
        """Empty request list → 0 total movement, empty service order."""
        result = fcfs([], INITIAL_HEAD, MIN_CYL, MAX_CYL)
        assert result.total_head_movement == 0
        assert result.service_order == []
        assert result.individual_movements == []

    def test_fcfs_single_request(self):
        """Single request [100] with head=50 → movement = |100-50| = 50."""
        result = fcfs([100], 50, MIN_CYL, MAX_CYL)
        assert result.service_order == [100]
        assert result.total_head_movement == 50
        assert result.individual_movements == [50]
        assert result.head_movement_path == [50, 100]

    def test_fcfs_head_at_first_request(self):
        """Head starts at first request position → first movement = 0."""
        result = fcfs([98, 183, 37], 98, MIN_CYL, MAX_CYL)
        # Path: 98 -> 98 -> 183 -> 37
        # Movements: |98-98|=0, |183-98|=85, |37-183|=146
        # Total: 0+85+146 = 231
        assert result.individual_movements[0] == 0
        assert result.total_head_movement == 0 + 85 + 146
        assert result.total_head_movement == 231

    def test_fcfs_duplicates(self):
        """Duplicate requests [50, 50, 50], head=40 → services all three."""
        result = fcfs([50, 50, 50], 40, MIN_CYL, MAX_CYL)
        # Path: 40 -> 50 -> 50 -> 50
        # Movements: |50-40|=10, |50-50|=0, |50-50|=0
        # Total: 10
        assert result.service_order == [50, 50, 50]
        assert len(result.service_order) == 3
        assert result.individual_movements == [10, 0, 0]
        assert result.total_head_movement == 10

    def test_fcfs_all_same_position(self):
        """All requests and head at same cylinder → 0 total movement."""
        result = fcfs([75, 75, 75], 75, MIN_CYL, MAX_CYL)
        assert result.total_head_movement == 0
        assert result.individual_movements == [0, 0, 0]

    def test_fcfs_head_at_boundary_zero(self):
        """Head at lower boundary (0)."""
        result = fcfs([50, 100], 0, MIN_CYL, MAX_CYL)
        # Path: 0 -> 50 -> 100
        # Movements: 50, 50
        # Total: 100
        assert result.total_head_movement == 100
        assert result.individual_movements == [50, 50]
        assert result.head_movement_path == [0, 50, 100]

    def test_fcfs_head_at_boundary_max(self):
        """Head at upper boundary (199)."""
        result = fcfs([100, 50], 199, MIN_CYL, MAX_CYL)
        # Path: 199 -> 100 -> 50
        # Movements: |100-199|=99, |50-100|=50
        # Total: 149
        assert result.total_head_movement == 149
        assert result.individual_movements == [99, 50]


class TestFCFSInvalidInputs:
    """Tests for invalid inputs — should raise ValueError."""

    def test_fcfs_invalid_request_out_of_range(self):
        """Request outside disk range should raise ValueError."""
        with pytest.raises(ValueError):
            fcfs([200], INITIAL_HEAD, MIN_CYL, MAX_CYL)

    def test_fcfs_invalid_request_negative(self):
        """Negative request should raise ValueError."""
        with pytest.raises(ValueError):
            fcfs([-1, 50], INITIAL_HEAD, MIN_CYL, MAX_CYL)

    def test_fcfs_invalid_head_position(self):
        """Head position outside disk range should raise ValueError."""
        with pytest.raises(ValueError):
            fcfs(REQUESTS, 250, MIN_CYL, MAX_CYL)

    def test_fcfs_invalid_head_position_negative(self):
        """Negative head position should raise ValueError."""
        with pytest.raises(ValueError):
            fcfs(REQUESTS, -10, MIN_CYL, MAX_CYL)
