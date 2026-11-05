"""
Comprehensive tests for SCAN (Elevator) disk scheduling algorithm.

Manual calculation for direction='left':
  requests = [98, 183, 37, 122, 14, 124, 65, 67], head = 53, disk 0-199
  Left of head (<=53): [37, 14] → sorted descending: [37, 14]
  Right of head (>53): [98, 183, 122, 124, 65, 67] → sorted ascending: [65, 67, 98, 122, 124, 183]
  Direction=left: serve left first (descending), reach boundary 0, reverse, serve right (ascending)
  Path:  53 → 37 → 14 → 0 → 65 → 67 → 98 → 122 → 124 → 183
  Moves: 16,  23,  14,  65,  2,   31,  24,   2,    59
  Total: 16+23+14+65+2+31+24+2+59 = 236
  Service order: [37, 14, 65, 67, 98, 122, 124, 183]

Manual calculation for direction='right':
  Right of head (>53): [65, 67, 98, 122, 124, 183] ascending
  Left of head (<=53): [37, 14] descending
  Direction=right: serve right first (ascending), reach boundary 199, reverse, serve left (descending)
  Path:  53 → 65 → 67 → 98 → 122 → 124 → 183 → 199 → 37 → 14
  Moves: 12,   2,  31,  24,    2,   59,   16, 162,  23
  Total: 12+2+31+24+2+59+16+162+23 = 331
  Service order: [65, 67, 98, 122, 124, 183, 37, 14]
"""

import sys
import pytest

sys.path.insert(0, r'c:\Users\adity\Desktop\ca-cse316')

from algorithms.scan import scan


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

class TestSCANLeft:
    """Tests for SCAN with direction='left'."""

    def test_scan_left_basic(self):
        """Verify path and total=236 for direction='left'."""
        result = scan(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL, direction='left')
        expected_path = [53, 37, 14, 0, 65, 67, 98, 122, 124, 183]
        expected_movements = [16, 23, 14, 65, 2, 31, 24, 2, 59]
        assert result.head_movement_path == expected_path
        assert result.individual_movements == expected_movements
        assert result.total_head_movement == 236

    def test_scan_left_service_order(self):
        """Service order for direction='left'."""
        result = scan(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL, direction='left')
        assert result.service_order == [37, 14, 65, 67, 98, 122, 124, 183]

    def test_scan_includes_boundary_left(self):
        """Path must include boundary 0 when direction='left'."""
        result = scan(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL, direction='left')
        assert 0 in result.head_movement_path


# ---------------------------------------------------------------------------
# Right direction tests
# ---------------------------------------------------------------------------

class TestSCANRight:
    """Tests for SCAN with direction='right'."""

    def test_scan_right_basic(self):
        """Verify path and total=331 for direction='right'."""
        result = scan(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL, direction='right')
        expected_path = [53, 65, 67, 98, 122, 124, 183, 199, 37, 14]
        expected_movements = [12, 2, 31, 24, 2, 59, 16, 162, 23]
        assert result.head_movement_path == expected_path
        assert result.individual_movements == expected_movements
        assert result.total_head_movement == 331

    def test_scan_right_service_order(self):
        """Service order for direction='right'."""
        result = scan(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL, direction='right')
        assert result.service_order == [65, 67, 98, 122, 124, 183, 37, 14]

    def test_scan_includes_boundary_right(self):
        """Path must include boundary 199 when direction='right'."""
        result = scan(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL, direction='right')
        assert 199 in result.head_movement_path


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestSCANEdgeCases:
    """Edge case tests for SCAN."""

    def test_scan_empty_requests(self):
        """Empty requests → 0 movement."""
        result = scan([], INITIAL_HEAD, MIN_CYL, MAX_CYL, direction='left')
        assert result.total_head_movement == 0
        assert result.service_order == []

    def test_scan_single_request(self):
        """Single request on the left side."""
        result = scan([30], 53, MIN_CYL, MAX_CYL, direction='left')
        # Direction=left: head goes left → 30 → 0  (but only 30 needs service)
        # Path: 53 → 30 → ... the head goes to 30, continues to 0, then reverses
        # Since no requests on right, path: 53 → 30 → 0
        # But 30 is the only request. Movements: 23, ... depends on boundary behavior
        # The request IS on the left, so it's served going left.
        assert 30 in result.service_order
        assert len(result.service_order) == 1

    def test_scan_all_left_direction_left(self):
        """All requests left of head, direction=left."""
        result = scan([10, 20, 30], 50, MIN_CYL, MAX_CYL, direction='left')
        # Left of head (<=50): [30, 20, 10] sorted descending
        # No right requests
        # Path: 50 → 30 → 20 → 10 → 0
        # Service order: [30, 20, 10]
        # Movements: 20, 10, 10, 10
        # Total: 50
        assert result.service_order == [30, 20, 10]
        assert result.total_head_movement == 50
        assert 0 in result.head_movement_path

    def test_scan_all_right_direction_left(self):
        """All requests right of head, direction=left → goes to 0 first, then right."""
        result = scan([100, 150, 180], 50, MIN_CYL, MAX_CYL, direction='left')
        # No left requests, but direction=left so head goes to 0 first, then reverses
        # Path: 50 → 0 → 100 → 150 → 180
        # Service order: [100, 150, 180]
        # Movements: 50, 100, 50, 30
        # Total: 230
        assert result.service_order == [100, 150, 180]
        assert result.total_head_movement == 230
        assert 0 in result.head_movement_path

    def test_scan_head_at_boundary_zero_left(self):
        """Head at boundary 0, direction=left → goes to 0 (already there), then right."""
        result = scan([50, 100], 0, MIN_CYL, MAX_CYL, direction='left')
        # Head=0, direction=left: already at boundary, reverse immediately
        # Path: 0 → 50 → 100
        # Service order: [50, 100]
        # Movements: 50, 50
        # Total: 100
        assert result.service_order == [50, 100]
        assert result.total_head_movement == 100

    def test_scan_head_at_boundary_max_right(self):
        """Head at boundary 199, direction=right → at boundary, reverse immediately."""
        result = scan([50, 100], 199, MIN_CYL, MAX_CYL, direction='right')
        # Head=199, direction=right: already at boundary, reverse
        # Path: 199 → 100 → 50
        # Service order: [100, 50]
        # Movements: 99, 50
        # Total: 149
        assert result.service_order == [100, 50]
        assert result.total_head_movement == 149

    def test_scan_duplicates(self):
        """Duplicate requests should all be serviced."""
        result = scan([50, 50, 100], 53, MIN_CYL, MAX_CYL, direction='left')
        # Left (<=53): [50, 50] sorted desc: [50, 50]
        # Right (>53): [100]
        # Path: 53 → 50 → 50 → 0 → 100
        # Service order: [50, 50, 100]
        # Movements: 3, 0, 50, 100
        # Total: 153
        assert len(result.service_order) == 3
        assert result.service_order.count(50) == 2
        assert result.total_head_movement == 153

    def test_scan_request_at_head(self):
        """Request equal to head position."""
        result = scan([53, 100], 53, MIN_CYL, MAX_CYL, direction='left')
        # 53 is <= head (equal), so it's on the left side
        # Left: [53] desc → [53]
        # Right: [100]
        # Path: 53 → 53 → 0 → 100
        # Movements: 0, 53, 100
        # Total: 153
        assert 53 in result.service_order
        assert len(result.service_order) == 2


class TestSCANInvalidInputs:
    """Invalid input tests."""

    def test_scan_invalid_direction(self):
        """Invalid direction should raise ValueError."""
        with pytest.raises(ValueError):
            scan(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL, direction='up')

    def test_scan_invalid_request(self):
        """Request out of range should raise ValueError."""
        with pytest.raises(ValueError):
            scan([200], INITIAL_HEAD, MIN_CYL, MAX_CYL, direction='left')

    def test_scan_invalid_head(self):
        """Head out of range should raise ValueError."""
        with pytest.raises(ValueError):
            scan(REQUESTS, 300, MIN_CYL, MAX_CYL, direction='left')
