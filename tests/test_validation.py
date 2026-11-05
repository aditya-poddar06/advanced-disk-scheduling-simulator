"""
Comprehensive tests for disk scheduling input validation functions.

Tests cover:
  - parse_request_string: comma, space, mixed separators, invalid, empty
  - validate_head_position: valid, boundary, out-of-range
  - validate_disk_range: valid, inverted, equal
  - validate_requests: in-range, out-of-range
  - validate_seek_time: positive, zero, negative
  - validate_all_inputs: combined validation
"""

import sys
import pytest

sys.path.insert(0, r'c:\Users\adity\Desktop\ca-cse316')

from core.validation import (
    parse_request_string,
    validate_head_position,
    validate_disk_range,
    validate_requests,
    validate_seek_time,
    validate_all_inputs,
)


# ---------------------------------------------------------------------------
# parse_request_string tests
# ---------------------------------------------------------------------------

class TestParseRequestString:

    def test_parse_comma_separated(self):
        """'98, 183, 37' → [98, 183, 37]"""
        result = parse_request_string("98, 183, 37")
        assert result == [98, 183, 37]

    def test_parse_space_separated(self):
        """'98 183 37' → [98, 183, 37]"""
        result = parse_request_string("98 183 37")
        assert result == [98, 183, 37]

    def test_parse_mixed_separators(self):
        """'98, 183 37' → [98, 183, 37]"""
        result = parse_request_string("98, 183 37")
        assert result == [98, 183, 37]

    def test_parse_invalid_string(self):
        """'abc' should raise ValueError."""
        with pytest.raises(ValueError):
            parse_request_string("abc")

    def test_parse_empty_string(self):
        """'' → []"""
        result = parse_request_string("")
        assert result == []

    def test_parse_single_value(self):
        """'42' → [42]"""
        result = parse_request_string("42")
        assert result == [42]

    def test_parse_extra_whitespace(self):
        """'  98 ,  183  , 37  ' → [98, 183, 37]"""
        result = parse_request_string("  98 ,  183  , 37  ")
        assert result == [98, 183, 37]


# ---------------------------------------------------------------------------
# validate_head_position tests
# ---------------------------------------------------------------------------

class TestValidateHeadPosition:

    def test_validate_head_valid(self):
        """53 in [0, 199] → True"""
        assert validate_head_position(53, 0, 199) is True

    def test_validate_head_at_lower_boundary(self):
        """0 in [0, 199] → True"""
        assert validate_head_position(0, 0, 199) is True

    def test_validate_head_at_upper_boundary(self):
        """199 in [0, 199] → True"""
        assert validate_head_position(199, 0, 199) is True

    def test_validate_head_invalid_above(self):
        """200 in [0, 199] → False"""
        assert validate_head_position(200, 0, 199) is False

    def test_validate_head_invalid_below(self):
        """-1 in [0, 199] → False"""
        assert validate_head_position(-1, 0, 199) is False


# ---------------------------------------------------------------------------
# validate_disk_range tests
# ---------------------------------------------------------------------------

class TestValidateDiskRange:

    def test_validate_disk_range_valid(self):
        """0, 199 → True"""
        assert validate_disk_range(0, 199) is True

    def test_validate_disk_range_invalid(self):
        """199, 0 → False (min > max)"""
        assert validate_disk_range(199, 0) is False

    def test_validate_disk_range_equal(self):
        """5, 5 → False (min == max, no range)"""
        assert validate_disk_range(5, 5) is False

    def test_validate_disk_range_small(self):
        """0, 1 → True (minimal valid range)"""
        assert validate_disk_range(0, 1) is True


# ---------------------------------------------------------------------------
# validate_requests tests
# ---------------------------------------------------------------------------

class TestValidateRequests:

    def test_validate_requests_valid(self):
        """[50, 100, 150] in [0, 199] → (True, ...)"""
        valid, msg = validate_requests([50, 100, 150], 0, 199)
        assert valid is True

    def test_validate_requests_out_of_range(self):
        """[200] in [0, 199] → (False, ...)"""
        valid, msg = validate_requests([200], 0, 199)
        assert valid is False

    def test_validate_requests_negative(self):
        """[-1] in [0, 199] → (False, ...)"""
        valid, msg = validate_requests([-1], 0, 199)
        assert valid is False

    def test_validate_requests_at_boundaries(self):
        """[0, 199] in [0, 199] → (True, ...)"""
        valid, msg = validate_requests([0, 199], 0, 199)
        assert valid is True

    def test_validate_requests_empty(self):
        """[] in [0, 199] → (True, ...)"""
        valid, msg = validate_requests([], 0, 199)
        assert valid is True


# ---------------------------------------------------------------------------
# validate_seek_time tests
# ---------------------------------------------------------------------------

class TestValidateSeekTime:

    def test_validate_seek_time_valid(self):
        """0.1 → True"""
        assert validate_seek_time(0.1) is True

    def test_validate_seek_time_zero(self):
        """0 → True"""
        assert validate_seek_time(0) is True

    def test_validate_seek_time_negative(self):
        """-1 → False"""
        assert validate_seek_time(-1) is False

    def test_validate_seek_time_large(self):
        """10.0 → True"""
        assert validate_seek_time(10.0) is True


# ---------------------------------------------------------------------------
# validate_all_inputs tests
# ---------------------------------------------------------------------------

class TestValidateAllInputs:

    def test_validate_all_valid(self):
        """All valid inputs → (True, [])"""
        valid, errors = validate_all_inputs(
            requests=[50, 100, 150],
            head=53,
            min_cyl=0,
            max_cyl=199,
            seek_time=0.1,
        )
        assert valid is True
        assert errors == []

    def test_validate_all_multiple_errors(self):
        """Multiple bad inputs → (False, [error messages])"""
        valid, errors = validate_all_inputs(
            requests=[200, -5],  # out of range
            head=300,            # out of range
            min_cyl=199,         # inverted range
            max_cyl=0,
            seek_time=-1,        # negative
        )
        assert valid is False
        assert len(errors) > 0
        # Should have multiple error messages
        assert isinstance(errors, list)
        for err in errors:
            assert isinstance(err, str)

    def test_validate_all_single_error_head(self):
        """Only head is invalid."""
        valid, errors = validate_all_inputs(
            requests=[50, 100],
            head=200,
            min_cyl=0,
            max_cyl=199,
            seek_time=0.1,
        )
        assert valid is False
        assert len(errors) >= 1

    def test_validate_all_single_error_seek(self):
        """Only seek_time is invalid."""
        valid, errors = validate_all_inputs(
            requests=[50, 100],
            head=53,
            min_cyl=0,
            max_cyl=199,
            seek_time=-0.5,
        )
        assert valid is False
        assert len(errors) >= 1
