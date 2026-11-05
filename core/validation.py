"""Input validation utilities for the UI layer of the disk scheduling simulator.

This module provides user-friendly validation and parsing functions designed
for use by graphical or command-line interfaces. It translates raw user input
(strings, numbers) into validated Python objects suitable for the simulation
engine.

These functions are separate from algorithms.common.validate_algorithm_inputs,
which performs algorithm-level validation. This module focuses on UI-level
concerns like parsing string input, providing human-readable error messages,
and aggregating multiple validation errors.
"""


def parse_request_string(request_string: str) -> list[int]:
    """Parse a string of comma or space separated integers into a list.

    Accepts integers separated by commas, spaces, or a mixture of both.
    Leading/trailing whitespace and empty tokens (from consecutive
    delimiters) are ignored.

    Args:
        request_string: A string containing integer values separated by
            commas and/or spaces. Examples: "98, 183, 37", "98 183 37",
            "98,183,37", "98, 183 37".

    Returns:
        list[int]: A list of parsed integer values. Returns an empty list
            if the input string is empty or contains only whitespace.

    Raises:
        ValueError: If any token in the string cannot be converted to an
            integer. The error message identifies the invalid token.

    Examples:
        >>> parse_request_string("98, 183, 37, 122")
        [98, 183, 37, 122]
        >>> parse_request_string("98 183 37")
        [98, 183, 37]
        >>> parse_request_string("")
        []
    """
    if not request_string or not request_string.strip():
        return []

    # Replace commas with spaces, then split on whitespace
    normalized: str = request_string.replace(",", " ")
    tokens: list[str] = normalized.split()

    result: list[int] = []
    for token in tokens:
        stripped: str = token.strip()
        if not stripped:
            continue
        try:
            result.append(int(stripped))
        except ValueError:
            raise ValueError(
                f"Invalid value '{stripped}' in request string. "
                f"All values must be integers."
            )

    return result


def validate_head_position(head: int, min_cyl: int, max_cyl: int) -> bool:
    """Check whether a head position is within the valid cylinder range.

    Args:
        head: The head position to validate.
        min_cyl: Minimum valid cylinder number.
        max_cyl: Maximum valid cylinder number.

    Returns:
        bool: True if head is an integer in [min_cyl, max_cyl], False otherwise.

    Examples:
        >>> validate_head_position(53, 0, 199)
        True
        >>> validate_head_position(200, 0, 199)
        False
    """
    if not isinstance(head, int) or isinstance(head, bool):
        return False
    return min_cyl <= head <= max_cyl


def validate_disk_range(min_cyl: int, max_cyl: int) -> bool:
    """Check whether a disk cylinder range is valid.

    A valid range requires both values to be non-negative integers with
    min_cyl strictly less than max_cyl.

    Args:
        min_cyl: Minimum cylinder number.
        max_cyl: Maximum cylinder number.

    Returns:
        bool: True if the range is valid, False otherwise.

    Examples:
        >>> validate_disk_range(0, 199)
        True
        >>> validate_disk_range(199, 0)
        False
        >>> validate_disk_range(-1, 199)
        False
    """
    if not isinstance(min_cyl, int) or isinstance(min_cyl, bool):
        return False
    if not isinstance(max_cyl, int) or isinstance(max_cyl, bool):
        return False
    if min_cyl < 0 or max_cyl < 0:
        return False
    return min_cyl < max_cyl


def validate_requests(
    requests: list[int],
    min_cyl: int,
    max_cyl: int,
) -> tuple[bool, str]:
    """Validate a list of disk I/O requests against the cylinder range.

    Checks that all values in the request list are integers within the
    specified cylinder range. An empty list is considered valid.

    Args:
        requests: List of cylinder numbers to validate.
        min_cyl: Minimum valid cylinder number.
        max_cyl: Maximum valid cylinder number.

    Returns:
        tuple[bool, str]: A tuple of (is_valid, error_message).
            Returns (True, '') if all requests are valid.
            Returns (False, error_message) with a descriptive error
            message for the first invalid request found.

    Examples:
        >>> validate_requests([98, 183, 37], 0, 199)
        (True, '')
        >>> validate_requests([98, 200], 0, 199)
        (False, 'Request 200 at index 1 is out of range [0, 199].')
    """
    for i, req in enumerate(requests):
        if not isinstance(req, int) or isinstance(req, bool):
            return (
                False,
                f"Request at index {i} is not an integer: {req}.",
            )
        if req < min_cyl or req > max_cyl:
            return (
                False,
                f"Request {req} at index {i} is out of range [{min_cyl}, {max_cyl}].",
            )
    return (True, "")


def validate_seek_time(seek_time: float) -> bool:
    """Check whether a seek time per cylinder value is valid.

    Args:
        seek_time: The seek time value to validate. Must be a non-negative
            number (int or float).

    Returns:
        bool: True if seek_time is a non-negative number, False otherwise.

    Examples:
        >>> validate_seek_time(0.1)
        True
        >>> validate_seek_time(0)
        True
        >>> validate_seek_time(-0.5)
        False
    """
    if isinstance(seek_time, bool):
        return False
    if not isinstance(seek_time, (int, float)):
        return False
    return seek_time >= 0


def validate_all_inputs(
    requests: list[int],
    head: int,
    min_cyl: int,
    max_cyl: int,
    seek_time: float,
) -> tuple[bool, list[str]]:
    """Validate all simulator inputs and collect all error messages.

    Performs comprehensive validation of all inputs needed to run the
    disk scheduling simulator. Unlike individual validation functions,
    this aggregates ALL errors rather than stopping at the first one.

    Args:
        requests: List of cylinder numbers for I/O requests.
        head: Initial head position.
        min_cyl: Minimum valid cylinder number.
        max_cyl: Maximum valid cylinder number.
        seek_time: Seek time per cylinder in milliseconds.

    Returns:
        tuple[bool, list[str]]: A tuple of (is_valid, error_messages).
            Returns (True, []) if all inputs are valid.
            Returns (False, [list_of_error_strings]) if any validation
            fails, with one error message per failed check.

    Examples:
        >>> validate_all_inputs([98, 183], 53, 0, 199, 0.1)
        (True, [])
        >>> valid, errors = validate_all_inputs([200], 53, 0, 199, -1.0)
        >>> valid
        False
        >>> len(errors)
        2
    """
    errors: list[str] = []

    # Validate disk range
    if not validate_disk_range(min_cyl, max_cyl):
        errors.append(
            f"Invalid disk range: min_cylinder ({min_cyl}) must be a "
            f"non-negative integer strictly less than max_cylinder ({max_cyl})."
        )

    # Validate head position (only meaningful if range is valid)
    if not validate_head_position(head, min_cyl, max_cyl):
        errors.append(
            f"Invalid head position: {head} must be an integer in "
            f"range [{min_cyl}, {max_cyl}]."
        )

    # Validate requests
    req_valid, req_error = validate_requests(requests, min_cyl, max_cyl)
    if not req_valid:
        errors.append(f"Invalid requests: {req_error}")

    # Validate seek time
    if not validate_seek_time(seek_time):
        errors.append(
            f"Invalid seek time: {seek_time} must be a non-negative number."
        )

    if errors:
        return (False, errors)
    return (True, [])
