"""Circular SCAN (C-SCAN) disk scheduling algorithm.

C-SCAN is a variant of SCAN that provides a more uniform wait time.
Instead of reversing direction at the boundary, the head jumps back to
the opposite boundary and continues servicing in the same direction.
This circular behavior ensures that all cylinders are treated more
equally in terms of wait time.
"""

from algorithms.common import SchedulingResult, validate_algorithm_inputs


def cscan(
    requests: list[int],
    initial_head: int,
    min_cylinder: int = 0,
    max_cylinder: int = 199,
    direction: str = "left",
) -> SchedulingResult:
    """Execute the Circular SCAN (C-SCAN) disk scheduling algorithm.

    The head moves in the given direction, servicing requests along the way,
    until it reaches the disk boundary. It then jumps (wraps) to the opposite
    boundary and continues servicing in the SAME direction.

    Boundary and wrap behavior:
        - The head travels to the boundary in the initial direction, even if
          no requests exist between the current position and that boundary.
        - After reaching the boundary, the head wraps to the opposite boundary.
          The wrap movement (max_cylinder - min_cylinder) IS counted in total
          head movement.
        - After wrapping, requests are serviced in the SAME direction as the
          initial direction.
        - Boundary cylinders are included in the path unless the head is
          already at that boundary.

    Request partitioning:
        - Requests equal to initial_head are classified as left_requests.

    Direction semantics after wrap:
        - direction='left': service descending, wrap min→max, continue descending
        - direction='right': service ascending, wrap max→min, continue ascending

    Args:
        requests: List of cylinder numbers to service. Duplicates are each
            serviced at their sorted position. An empty list yields zero
            head movement.
        initial_head: Starting cylinder position of the disk head.
        min_cylinder: Minimum valid cylinder number on the disk. Defaults to 0.
        max_cylinder: Maximum valid cylinder number on the disk. Defaults to 199.
        direction: Initial direction of head movement, either 'left'
            (toward min_cylinder) or 'right' (toward max_cylinder).
            Defaults to 'left'.

    Returns:
        SchedulingResult: A result object containing:
            - algorithm_name: 'C-SCAN'
            - request_sequence: Copy of the original requests
            - service_order: Requests in the order they were serviced
            - head_movement_path: Full trajectory including boundary and wrap
            - individual_movements: Absolute movement for each step (wrap included)
            - total_head_movement: Sum of all individual movements
            - direction: The initial direction used

    Raises:
        ValueError: If inputs fail validation or direction is invalid.

    Examples:
        >>> result = cscan([98, 183, 37, 122], 53, direction='left')
        >>> # Path: 53 -> 37 -> 0 -> 199 -> 183 -> 122 -> 98
        >>> result.service_order
        [37, 183, 122, 98]
    """
    validate_algorithm_inputs(requests, initial_head, min_cylinder, max_cylinder)

    if direction not in ("left", "right"):
        raise ValueError(
            f"direction must be 'left' or 'right', got '{direction}'"
        )

    # Handle empty requests
    if not requests:
        return SchedulingResult(
            algorithm_name="C-SCAN",
            request_sequence=list(requests),
            service_order=[],
            head_movement_path=[initial_head],
            individual_movements=[],
            total_head_movement=0,
            direction=direction,
        )

    # Partition requests: <= initial_head go left, > initial_head go right
    left_requests_desc: list[int] = sorted(
        [r for r in requests if r <= initial_head], reverse=True
    )
    right_requests_asc: list[int] = sorted(
        [r for r in requests if r > initial_head]
    )

    # Build the service order and head movement path
    service_order: list[int] = []
    head_movement_path: list[int] = [initial_head]

    if direction == "left":
        # Phase 1: Move left — service left_requests in descending order
        service_order.extend(left_requests_desc)
        head_movement_path.extend(left_requests_desc)

        # Travel to min_cylinder boundary (if not already there)
        if head_movement_path[-1] != min_cylinder:
            head_movement_path.append(min_cylinder)

        # Phase 2: Circular wrap — jump from min_cylinder to max_cylinder
        # Only add if we have requests on the other side to service
        if right_requests_asc:
            head_movement_path.append(max_cylinder)

            # Continue in SAME direction (left/descending) through right_requests
            right_requests_desc: list[int] = sorted(
                right_requests_asc, reverse=True
            )
            service_order.extend(right_requests_desc)
            head_movement_path.extend(right_requests_desc)

    else:  # direction == "right"
        # Phase 1: Move right — service right_requests in ascending order
        service_order.extend(right_requests_asc)
        head_movement_path.extend(right_requests_asc)

        # Travel to max_cylinder boundary (if not already there)
        if head_movement_path[-1] != max_cylinder:
            head_movement_path.append(max_cylinder)

        # Phase 2: Circular wrap — jump from max_cylinder to min_cylinder
        if left_requests_desc:
            head_movement_path.append(min_cylinder)

            # Continue in SAME direction (right/ascending) through left_requests
            left_requests_asc: list[int] = sorted(left_requests_desc)
            service_order.extend(left_requests_asc)
            head_movement_path.extend(left_requests_asc)

    # Calculate individual movements from the complete path
    individual_movements: list[int] = [
        abs(head_movement_path[i + 1] - head_movement_path[i])
        for i in range(len(head_movement_path) - 1)
    ]

    total_head_movement: int = sum(individual_movements)

    return SchedulingResult(
        algorithm_name="C-SCAN",
        request_sequence=list(requests),
        service_order=service_order,
        head_movement_path=head_movement_path,
        individual_movements=individual_movements,
        total_head_movement=total_head_movement,
        direction=direction,
    )
