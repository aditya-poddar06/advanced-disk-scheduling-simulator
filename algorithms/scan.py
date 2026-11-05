"""SCAN (Elevator) disk scheduling algorithm.

The SCAN algorithm moves the disk head in one direction, servicing all
requests along the way, until it reaches the disk boundary. It then
reverses direction and services the remaining requests. This is analogous
to an elevator that goes all the way up before coming back down.
"""

from algorithms.common import SchedulingResult, validate_algorithm_inputs


def scan(
    requests: list[int],
    initial_head: int,
    min_cylinder: int = 0,
    max_cylinder: int = 199,
    direction: str = "left",
) -> SchedulingResult:
    """Execute the SCAN (Elevator) disk scheduling algorithm.

    The head moves in the given direction, servicing requests along the way,
    until it reaches the disk boundary. It then reverses and services
    remaining requests in the opposite direction.

    Boundary behavior:
        - The head always travels to the boundary in the initial direction,
          even if there are no requests between the current position and that
          boundary.
        - The boundary cylinder is included in the head_movement_path unless
          the head is already at that boundary position.

    Request partitioning:
        - Requests equal to initial_head are classified as left_requests
          (i.e., they go into the <= partition).

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
            - algorithm_name: 'SCAN'
            - request_sequence: Copy of the original requests
            - service_order: Requests in the order they were serviced
            - head_movement_path: Full trajectory including boundary positions
            - individual_movements: Absolute movement for each step
            - total_head_movement: Sum of all individual movements
            - direction: The initial direction used

    Raises:
        ValueError: If inputs fail validation or direction is invalid.

    Examples:
        >>> result = scan([98, 183, 37, 122], 53, direction='left')
        >>> result.head_movement_path
        [53, 37, 0, 98, 122, 183]
    """
    validate_algorithm_inputs(requests, initial_head, min_cylinder, max_cylinder)

    if direction not in ("left", "right"):
        raise ValueError(
            f"direction must be 'left' or 'right', got '{direction}'"
        )

    # Handle empty requests
    if not requests:
        return SchedulingResult(
            algorithm_name="SCAN",
            request_sequence=list(requests),
            service_order=[],
            head_movement_path=[initial_head],
            individual_movements=[],
            total_head_movement=0,
            direction=direction,
        )

    # Partition requests: <= initial_head go left, > initial_head go right
    left_requests: list[int] = sorted(
        [r for r in requests if r <= initial_head], reverse=True
    )
    right_requests: list[int] = sorted(
        [r for r in requests if r > initial_head]
    )

    # Build the service order and head movement path
    service_order: list[int] = []
    head_movement_path: list[int] = [initial_head]

    if direction == "left":
        # Move left: service left_requests in descending order
        service_order.extend(left_requests)
        head_movement_path.extend(left_requests)

        # Travel to min_cylinder boundary (if not already there)
        last_pos = head_movement_path[-1]
        if last_pos != min_cylinder:
            head_movement_path.append(min_cylinder)

        # Reverse: service right_requests in ascending order
        service_order.extend(right_requests)
        head_movement_path.extend(right_requests)

    else:  # direction == "right"
        # Move right: service right_requests in ascending order
        service_order.extend(right_requests)
        head_movement_path.extend(right_requests)

        # Travel to max_cylinder boundary (if not already there)
        last_pos = head_movement_path[-1]
        if last_pos != max_cylinder:
            head_movement_path.append(max_cylinder)

        # Reverse: service left_requests in descending order
        service_order.extend(left_requests)
        head_movement_path.extend(left_requests)

    # Calculate individual movements from the complete path
    individual_movements: list[int] = [
        abs(head_movement_path[i + 1] - head_movement_path[i])
        for i in range(len(head_movement_path) - 1)
    ]

    total_head_movement: int = sum(individual_movements)

    return SchedulingResult(
        algorithm_name="SCAN",
        request_sequence=list(requests),
        service_order=service_order,
        head_movement_path=head_movement_path,
        individual_movements=individual_movements,
        total_head_movement=total_head_movement,
        direction=direction,
    )
