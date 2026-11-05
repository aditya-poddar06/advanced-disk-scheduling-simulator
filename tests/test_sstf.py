"""
Comprehensive tests for SSTF (Shortest Seek Time First) disk scheduling algorithm.

Manual calculations for standard test case:
  requests = [98, 183, 37, 122, 14, 124, 65, 67], initial_head = 53, disk 0-199

  Step-by-step closest selection:
    Head=53:  pending=[98,183,37,122,14,124,65,67]
              distances=[45,130,16,69,39,71,12,14]  → closest=65 (dist=12)
    Head=65:  pending=[98,183,37,122,14,124,67]
              distances=[33,118,28,57,51,59,2]      → closest=67 (dist=2)
    Head=67:  pending=[98,183,37,122,14,124]
              distances=[31,116,30,55,53,57]         → closest=37 (dist=30)
    Head=37:  pending=[98,183,122,14,124]
              distances=[61,146,85,23,87]            → closest=14 (dist=23)
    Head=14:  pending=[98,183,122,124]
              distances=[84,169,108,110]             → closest=98 (dist=84)
    Head=98:  pending=[183,122,124]
              distances=[85,24,26]                   → closest=122 (dist=24)
    Head=122: pending=[183,124]
              distances=[61,2]                       → closest=124 (dist=2)
    Head=124: pending=[183]
              distances=[59]                         → closest=183 (dist=59)

  Service order: [65, 67, 37, 14, 98, 122, 124, 183]
  Individual movements: [12, 2, 30, 23, 84, 24, 2, 59]
  Total: 12+2+30+23+84+24+2+59 = 236
"""

import sys
import pytest

sys.path.insert(0, r'c:\Users\adity\Desktop\ca-cse316')

from algorithms.sstf import sstf


# ---------------------------------------------------------------------------
# Standard test data
# ---------------------------------------------------------------------------
REQUESTS = [98, 183, 37, 122, 14, 124, 65, 67]
INITIAL_HEAD = 53
MIN_CYL = 0
MAX_CYL = 199

EXPECTED_SERVICE_ORDER = [65, 67, 37, 14, 98, 122, 124, 183]
EXPECTED_INDIVIDUAL_MOVEMENTS = [12, 2, 30, 23, 84, 24, 2, 59]
EXPECTED_TOTAL = 236


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestSSTFBasic:
    """Basic correctness tests with manually-calculated expected values."""

    def test_sstf_basic(self):
        """Verify service order matches SSTF greedy nearest-selection."""
        result = sstf(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL)
        assert result.service_order == EXPECTED_SERVICE_ORDER

    def test_sstf_total_movement(self):
        """Total head movement = 236 for the standard test case."""
        result = sstf(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL)
        assert result.total_head_movement == EXPECTED_TOTAL

    def test_sstf_individual_movements(self):
        """Each step's individual movement matches manual calculation."""
        result = sstf(REQUESTS, INITIAL_HEAD, MIN_CYL, MAX_CYL)
        assert result.individual_movements == EXPECTED_INDIVIDUAL_MOVEMENTS
        # Verify sum consistency
        assert sum(result.individual_movements) == result.total_head_movement


class TestSSTFEdgeCases:
    """Edge case tests for SSTF."""

    def test_sstf_empty_requests(self):
        """Empty request list → 0 total movement."""
        result = sstf([], INITIAL_HEAD, MIN_CYL, MAX_CYL)
        assert result.total_head_movement == 0
        assert result.service_order == []
        assert result.individual_movements == []

    def test_sstf_single_request(self):
        """Single request [100] with head=50 → movement = 50."""
        result = sstf([100], 50, MIN_CYL, MAX_CYL)
        assert result.service_order == [100]
        assert result.total_head_movement == 50
        assert result.individual_movements == [50]

    def test_sstf_duplicates(self):
        """Duplicate requests [50, 50] with head=40 → services both."""
        result = sstf([50, 50], 40, MIN_CYL, MAX_CYL)
        # Path: 40 -> 50 -> 50
        # Movements: 10, 0
        # Total: 10
        assert result.service_order == [50, 50]
        assert len(result.service_order) == 2
        assert result.total_head_movement == 10
        assert result.individual_movements == [10, 0]

    def test_sstf_tie_breaking(self):
        """Two equidistant requests: [40, 60], head=50 → tie-break to lower (40)."""
        result = sstf([40, 60], 50, MIN_CYL, MAX_CYL)
        # Both at distance 10 from head=50
        # Tie-breaking: choose lower cylinder (40) first
        # Path: 50 -> 40 -> 60
        # Movements: 10, 20
        # Total: 30
        assert result.service_order == [40, 60]
        assert result.total_head_movement == 30
        assert result.individual_movements == [10, 20]

    def test_sstf_all_one_side(self):
        """All requests on one side of head."""
        result = sstf([100, 120, 150, 180], 50, MIN_CYL, MAX_CYL)
        # Closest first from 50: 100(50), 120(70), 150(100), 180(130)
        # After servicing 100, next closest is 120 (dist=20), then 150 (30), then 180 (30)
        # Service order: [100, 120, 150, 180]
        # Path: 50 -> 100 -> 120 -> 150 -> 180
        # Movements: 50, 20, 30, 30
        # Total: 130
        assert result.service_order == [100, 120, 150, 180]
        assert result.total_head_movement == 130
        assert result.individual_movements == [50, 20, 30, 30]

    def test_sstf_head_at_request(self):
        """Head starts at a request position → that request is served first with 0 movement."""
        result = sstf([53, 100, 20], 53, MIN_CYL, MAX_CYL)
        # Head=53, request at 53 has distance 0 → served first
        # Then pending=[100, 20]: from 53, dist to 100=47, dist to 20=33 → choose 20
        # Then pending=[100]: dist=80
        # Service order: [53, 20, 100]
        # Movements: 0, 33, 80
        # Total: 113
        assert result.service_order[0] == 53
        assert result.individual_movements[0] == 0
        assert result.total_head_movement == 113

    def test_sstf_all_same_position(self):
        """All requests at same position."""
        result = sstf([75, 75, 75], 75, MIN_CYL, MAX_CYL)
        assert result.total_head_movement == 0
        assert result.service_order == [75, 75, 75]


class TestSSTFInvalidInputs:
    """Invalid input tests — should raise ValueError."""

    def test_sstf_invalid_request_out_of_range(self):
        """Request outside disk range should raise ValueError."""
        with pytest.raises(ValueError):
            sstf([200], INITIAL_HEAD, MIN_CYL, MAX_CYL)

    def test_sstf_invalid_head_position(self):
        """Head position outside disk range should raise ValueError."""
        with pytest.raises(ValueError):
            sstf(REQUESTS, 250, MIN_CYL, MAX_CYL)

    def test_sstf_invalid_negative_request(self):
        """Negative request should raise ValueError."""
        with pytest.raises(ValueError):
            sstf([-5, 50], INITIAL_HEAD, MIN_CYL, MAX_CYL)
