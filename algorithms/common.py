"""Common data structures and validation utilities for disk scheduling algorithms.

This module provides the shared SchedulingResult dataclass used by all algorithm
implementations, as well as input validation logic to ensure correctness before
any scheduling computation begins.
"""

from dataclasses import dataclass, field


@dataclass
class SchedulingResult:
    """Encapsulates the complete result of a disk scheduling algorithm execution.

    Attributes:
        algorithm_name: Name of the algorithm that produced this result
            (e.g., 'FCFS', 'SSTF', 'SCAN', 'C-SCAN').
        request_sequence: The original list of disk I/O requests as provided
            by the caller, in their original order.
        service_order: The order in which requests were actually serviced
            by the algorithm. May differ from request_sequence for algorithms
            that reorder requests (e.g., SSTF, SCAN).
        head_movement_path: The full trajectory of the disk head, starting
            with the initial head position. For SCAN/C-SCAN, this includes
            boundary cylinder positions where the head reverses or wraps.
        individual_movements: A list of absolute head movements for each
            consecutive step in head_movement_path. Length is
            len(head_movement_path) - 1.
        total_head_movement: The sum of all individual movements, representing
            the total number of cylinders traversed.
        direction: The initial direction of head movement for directional
            algorithms ('left' or 'right'). None for non-directional algorithms
            like FCFS and SSTF.
    """

    algorithm_name: str = ""
    request_sequence: list[int] = field(default_factory=list)
    service_order: list[int] = field(default_factory=list)
    head_movement_path: list[int] = field(default_factory=list)
    individual_movements: list[int] = field(default_factory=list)
    total_head_movement: int = 0
    direction: str | None = None


def validate_algorithm_inputs(
    requests: list[int],
    initial_head: int,
    min_cylinder: int,
    max_cylinder: int,
) -> None:
    """Validate all inputs for a disk scheduling algorithm.

    Checks that the cylinder range, initial head position, and all request
    values are within acceptable bounds. Raises ValueError with a descriptive
    message on the first validation failure encountered.

    Args:
        requests: List of cylinder numbers representing I/O requests.
        initial_head: Starting position of the disk read/write head.
        min_cylinder: Minimum valid cylinder number on the disk.
        max_cylinder: Maximum valid cylinder number on the disk.

    Raises:
        ValueError: If any of the following conditions are violated:
            - min_cylinder or max_cylinder is not a non-negative integer.
            - min_cylinder is not strictly less than max_cylinder.
            - initial_head is outside [min_cylinder, max_cylinder].
            - Any request value is not an integer.
            - Any request value is outside [min_cylinder, max_cylinder].
    """
    # Validate min_cylinder and max_cylinder are non-negative integers
    if not isinstance(min_cylinder, int) or isinstance(min_cylinder, bool):
        raise ValueError(
            f"min_cylinder must be a non-negative integer, got {type(min_cylinder).__name__}: {min_cylinder}"
        )
    if not isinstance(max_cylinder, int) or isinstance(max_cylinder, bool):
        raise ValueError(
            f"max_cylinder must be a non-negative integer, got {type(max_cylinder).__name__}: {max_cylinder}"
        )
    if min_cylinder < 0:
        raise ValueError(
            f"min_cylinder must be non-negative, got {min_cylinder}"
        )
    if max_cylinder < 0:
        raise ValueError(
            f"max_cylinder must be non-negative, got {max_cylinder}"
        )

    # Validate range ordering
    if min_cylinder >= max_cylinder:
        raise ValueError(
            f"min_cylinder ({min_cylinder}) must be strictly less than "
            f"max_cylinder ({max_cylinder})"
        )

    # Validate initial_head is an integer in range
    if not isinstance(initial_head, int) or isinstance(initial_head, bool):
        raise ValueError(
            f"initial_head must be an integer, got {type(initial_head).__name__}: {initial_head}"
        )
    if initial_head < min_cylinder or initial_head > max_cylinder:
        raise ValueError(
            f"initial_head ({initial_head}) must be in range "
            f"[{min_cylinder}, {max_cylinder}]"
        )

    # Validate each request
    for i, req in enumerate(requests):
        if not isinstance(req, int) or isinstance(req, bool):
            raise ValueError(
                f"All requests must be integers. Request at index {i} is "
                f"{type(req).__name__}: {req}"
            )
        if req < min_cylinder or req > max_cylinder:
            raise ValueError(
                f"Request at index {i} ({req}) is out of range "
                f"[{min_cylinder}, {max_cylinder}]"
            )
