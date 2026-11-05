"""
Comprehensive tests for C-SCAN (Circular SCAN) disk scheduling algorithm.

Manual calculation for direction='left':
  requests = [98, 183, 37, 122, 14, 124, 65, 67], head = 53, disk 0-199
  Left of head (<=53): [37, 14] → descending: [37, 14]
  Right of head (>53): [183, 124, 122, 98, 67, 65] → descending (served after wrap)
  Direction=left: service left descending, reach 0, wrap to 199, service remaining descending
  Path:  53 → 37 → 14 → 0 → 199 → 183 → 124 → 122 → 98 → 67 → 65
  Moves: 16,  23,  14, 199,  16,   59,    2,   24,  31,   2
  Total: 16+23+14+199+16+59+2+24+31+2 = 386
  Service order: [37, 14, 183, 124, 122, 98, 67, 65]

Manual calculation for direction='right':
  Right of head (>53): [65, 67, 98, 122, 124, 183] ascending
  Left of head (<=53): [14, 37] ascending (after wrap, continue ascending/right)
  Direction=right: service right ascending, reach 199, wrap to 0, service remaining ascending
  Path:  53 → 65 → 67 → 98 → 122 → 124 → 183 → 199 → 0 → 14 → 37
  Moves: 12,   2,  31,  24,    2,   59,   16, 199,  14,  23
  Total: 12+2+31+24+2+59+16+199+14+23 = 382
  Service order: [65, 67, 98, 122, 124, 183, 14, 37]
"""

import sys
import pytest

sys.path.insert(0, r'c:\Users\adity\Desktop\ca-cse316')

from algorithms.cscan import cscan


# ---------------------------------------------------------------------------
# Standard test data
# ---------------------------------------------------------------------------
REQUESTS = [98, 183, 37, 122, 14, 124, 65, 67]
INITIAL_HEAD = 53
MIN_CYL = 0
MAX_CYL = 199


# ---------------------------------------------------------------------------
# Left direction tests
# ---------------------------------------------------------------------------

class TestCSCANLeft:
    """Tests for C-SCAN with direction='left'."""

    def test_cscan_left_basic(self):
        """Verify path and total=386 for direction='left'."""
        result = cscan(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL, direction='left')
        expected_path = [53, 37, 14, 0, 199, 183, 124, 122, 98, 67, 65]
        expected_movements = [16, 23, 14, 199, 16, 59, 2, 24, 31, 2]
        assert result.head_movement_path == expected_path
        assert result.individual_movements == expected_movements
        assert result.total_head_movement == 386

    def test_cscan_left_service_order(self):
        """Service order for direction='left'."""
        result = cscan(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL, direction='left')
        assert result.service_order == [37, 14, 183, 124, 122, 98, 67, 65]

    def test_cscan_left_includes_both_boundaries(self):
        """Path must include both 0 and 199 for C-SCAN left."""
        result = cscan(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL, direction='left')
        assert 0 in result.head_movement_path
        assert 199 in result.head_movement_path


# ---------------------------------------------------------------------------
# Right direction tests
# ---------------------------------------------------------------------------

class TestCSCANRight:
    """Tests for C-SCAN with direction='right'."""

    def test_cscan_right_basic(self):
        """Verify path and total=382 for direction='right'."""
        result = cscan(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL, direction='right')
        expected_path = [53, 65, 67, 98, 122, 124, 183, 199, 0, 14, 37]
        expected_movements = [12, 2, 31, 24, 2, 59, 16, 199, 14, 23]
        assert result.head_movement_path == expected_path
        assert result.individual_movements == expected_movements
        assert result.total_head_movement == 382

    def test_cscan_right_service_order(self):
        """Service order for direction='right'."""
        result = cscan(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL, direction='right')
        assert result.service_order == [65, 67, 98, 122, 124, 183, 14, 37]

    def test_cscan_right_includes_both_boundaries(self):
        """Path must include both 0 and 199 for C-SCAN right."""
        result = cscan(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL, direction='right')
        assert 0 in result.head_movement_path
        assert 199 in result.head_movement_path


# ---------------------------------------------------------------------------
# Circular wrap verification
# ---------------------------------------------------------------------------

class TestCSCANWrap:
    """Verify the circular wrap contributes to total movement."""

    def test_cscan_circular_wrap_counted_left(self):
        """The 199-unit wrap (0→199) is included in the total for direction='left'."""
        result = cscan(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL, direction='left')
        # The wrap from 0 → 199 is 199 units
        assert 199 in result.individual_movements
        assert sum(result.individual_movements) == result.total_head_movement

    def test_cscan_circular_wrap_counted_right(self):
        """The 199-unit wrap (199→0) is included in the total for direction='right'."""
        result = cscan(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL, direction='right')
        # The wrap from 199 → 0 is 199 units
        assert 199 in result.individual_movements
        assert sum(result.individual_movements) == result.total_head_movement


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestCSCANEdgeCases:
    """Edge case tests for C-SCAN."""

    def test_cscan_empty_requests(self):
        """Empty requests → 0 movement."""
        result = cscan([], INITIAL_HEAD, MIN_CYL, MAX_CYL, direction='left')
        assert result.total_head_movement == 0
        assert result.service_order == []

    def test_cscan_single_request_left(self):
        """Single request on the left side, direction=left."""
        result = cscan([30], 53, MIN_CYL, MAX_CYL, direction='left')
        # Direction=left: 53 → 30 → 0 (no wrap needed since only left request)
        # OR if always wraps: depends on implementation
        assert 30 in result.service_order
        assert len(result.service_order) == 1

    def test_cscan_single_request_right(self):
        """Single request on the right side, direction=right."""
        result = cscan([100], 53, MIN_CYL, MAX_CYL, direction='right')
        # Direction=right: 53 → 100 → ... (no wrap needed since only right request)
        assert 100 in result.service_order
        assert len(result.service_order) == 1

    def test_cscan_all_one_side_left(self):
        """All requests left of head, direction=left."""
        result = cscan([10, 20, 30], 50, MIN_CYL, MAX_CYL, direction='left')
        # Left: [30, 20, 10] descending
        # No right requests, so no wrap needed
        # Path: 50 → 30 → 20 → 10 → 0
        # Service order: [30, 20, 10]
        # Movements: 20, 10, 10, 10
        # Total: 50
        assert result.service_order == [30, 20, 10]
        assert len(result.service_order) == 3

    def test_cscan_all_one_side_right(self):
        """All requests right of head, direction=right."""
        result = cscan([100, 150, 180], 50, MIN_CYL, MAX_CYL, direction='right')
        # Right: [100, 150, 180] ascending
        # No left requests, so no wrap needed
        # Path: 50 → 100 → 150 → 180
        # But C-SCAN may still go to 199. Implementation dependent.
        assert len(result.service_order) == 3

    def test_cscan_head_at_boundary_zero(self):
        """Head at lower boundary 0."""
        result = cscan([50, 100], 0, MIN_CYL, MAX_CYL, direction='left')
        # Head=0, direction=left: at boundary already, wraps to 199, services descending
        # Requests > 0: [50, 100] → descending [100, 50]
        # Path: 0 → 199 → 100 → 50  (wraps)
        # OR if no left requests: serves right side
        assert len(result.service_order) == 2

    def test_cscan_head_at_boundary_max(self):
        """Head at upper boundary 199."""
        result = cscan([50, 100], 199, MIN_CYL, MAX_CYL, direction='right')
        # Head=199, direction=right: at boundary, wraps to 0, services ascending
        # Requests < 199: [50, 100] → ascending [50, 100]
        # Path: 199 → 0 → 50 → 100
        assert len(result.service_order) == 2

    def test_cscan_duplicates(self):
        """Duplicate requests should all be serviced."""
        result = cscan([50, 50, 100], 53, MIN_CYL, MAX_CYL, direction='right')
        assert len(result.service_order) == 3
        assert result.service_order.count(50) == 2


class TestCSCANInvalidInputs:
    """Invalid input tests."""

    def test_cscan_invalid_direction(self):
        """Invalid direction should raise ValueError."""
        with pytest.raises(ValueError):
            cscan(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL, direction='up')

    def test_cscan_invalid_request(self):
        """Request out of range should raise ValueError."""
        with pytest.raises(ValueError):
            cscan([200], INITIAL_HEAD, MIN_CYL, MAX_CYL, direction='left')

    def test_cscan_invalid_head(self):
        """Head out of range should raise ValueError."""
        with pytest.raises(ValueError):
            cscan(REQUESTS, 300, MIN_CYL, MAX_CYL, direction='left')
