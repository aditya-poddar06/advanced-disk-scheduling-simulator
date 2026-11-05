"""Shortest Seek Time First (SSTF) disk scheduling algorithm.

SSTF selects the pending request closest to the current head position at
each step, minimizing individual seek times greedily. While it reduces
average seek time compared to FCFS, it can cause starvation for requests
far from the head.
"""

from algorithms.common import SchedulingResult, validate_algorithm_inputs


def sstf(
    requests: list[int],
    initial_head: int,
    min_cylinder: int = 0,
    max_cylinder: int = 199,
) -> SchedulingResult:
    """Execute the Shortest Seek Time First disk scheduling algorithm.

    At each step, the algorithm selects the pending request that requires
    the smallest head movement (shortest seek) from the current position.

    Tie-breaking rule: When two or more requests are equidistant from the
    current head position, the request with the LOWER cylinder number is
    chosen first.

    Args:
        requests: List of cylinder numbers to service. Duplicates are
            tracked independently using indices—each occurrence is serviced
            separately. An empty list results in zero head movement.
        initial_head: Starting cylinder position of the disk head.
        min_cylinder: Minimum valid cylinder number on the disk. Defaults to 0.
        max_cylinder: Maximum valid cylinder number on the disk. Defaults to 199.

    Returns:
        SchedulingResult: A result object containing:
            - algorithm_name: 'SSTF'
            - request_sequence: Copy of the original requests
            - service_order: Requests ordered by shortest seek from each position
            - head_movement_path: [initial_head, first_serviced, second_serviced, ...]
            - individual_movements: Absolute movement for each step
            - total_head_movement: Sum of all individual movements
            - direction: None (SSTF is non-directional)

    Raises:
        ValueError: If inputs fail validation (see validate_algorithm_inputs).

    Examples:
        >>> result = sstf([98, 183, 37, 122], 53)
        >>> result.service_order
        [37, 98, 122, 183]
    """
    validate_algorithm_inputs(requests, initial_head, min_cylinder, max_cylinder)

    # Handle empty requests
    if not requests:
        return SchedulingResult(
            algorithm_name="SSTF",
            request_sequence=list(requests),
            service_order=[],
            head_movement_path=[initial_head],
            individual_movements=[],
            total_head_movement=0,
            direction=None,
        )

    # Track pending requests by index so duplicates are handled correctly
    pending_indices: list[int] = list(range(len(requests)))
    current_head: int = initial_head
    service_order: list[int] = []
    head_movement_path: list[int] = [initial_head]
    individual_movements: list[int] = []

    while pending_indices:
        # Find the closest pending request
        # Tie-breaking: lower cylinder number wins (min on (distance, cylinder))
        best_idx: int = min(
            pending_indices,
            key=lambda idx: (abs(requests[idx] - current_head), requests[idx]),
        )

        # Service the chosen request
        chosen_cylinder: int = requests[best_idx]
        movement: int = abs(chosen_cylinder - current_head)

        service_order.append(chosen_cylinder)
        head_movement_path.append(chosen_cylinder)
        individual_movements.append(movement)

        current_head = chosen_cylinder
        pending_indices.remove(best_idx)

    total_head_movement: int = sum(individual_movements)

    return SchedulingResult(
        algorithm_name="SSTF",
        request_sequence=list(requests),
        service_order=service_order,
        head_movement_path=head_movement_path,
        individual_movements=individual_movements,
        total_head_movement=total_head_movement,
        direction=None,
    )
