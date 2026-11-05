"""First-Come, First-Served (FCFS) disk scheduling algorithm.

FCFS is the simplest disk scheduling algorithm. It processes I/O requests
in exactly the order they arrive, without any reordering or optimization.
While fair, it can result in large total head movements due to the lack
of seek optimization.
"""

from algorithms.common import SchedulingResult, validate_algorithm_inputs


def fcfs(
    requests: list[int],
    initial_head: int,
    min_cylinder: int = 0,
    max_cylinder: int = 199,
) -> SchedulingResult:
    """Execute the First-Come, First-Served disk scheduling algorithm.

    Processes disk I/O requests in their exact arrival order. The disk head
    moves from its initial position to the first request, then to the second,
    and so on, without any reordering.

    Args:
        requests: List of cylinder numbers to service, processed in order.
            May contain duplicates; each occurrence is serviced individually.
            An empty list is valid and results in zero head movement.
        initial_head: Starting cylinder position of the disk head.
        min_cylinder: Minimum valid cylinder number on the disk. Defaults to 0.
        max_cylinder: Maximum valid cylinder number on the disk. Defaults to 199.

    Returns:
        SchedulingResult: A result object containing:
            - algorithm_name: 'FCFS'
            - request_sequence: Copy of the original requests
            - service_order: Same as request_sequence (no reordering)
            - head_movement_path: [initial_head, req0, req1, ..., reqN]
            - individual_movements: Absolute movement for each step
            - total_head_movement: Sum of all individual movements
            - direction: None (FCFS is non-directional)

    Raises:
        ValueError: If inputs fail validation (see validate_algorithm_inputs).

    Examples:
        >>> result = fcfs([98, 183, 37, 122], 53)
        >>> result.total_head_movement
        640
        >>> result.service_order
        [98, 183, 37, 122]
    """
    validate_algorithm_inputs(requests, initial_head, min_cylinder, max_cylinder)

    # Handle empty requests
    if not requests:
        return SchedulingResult(
            algorithm_name="FCFS",
            request_sequence=list(requests),
            service_order=[],
            head_movement_path=[initial_head],
            individual_movements=[],
            total_head_movement=0,
            direction=None,
        )

    # Build the head movement path: initial position followed by each request
    head_movement_path: list[int] = [initial_head] + list(requests)

    # Calculate individual movements between consecutive positions
    individual_movements: list[int] = [
        abs(head_movement_path[i + 1] - head_movement_path[i])
        for i in range(len(head_movement_path) - 1)
    ]

    total_head_movement: int = sum(individual_movements)

    return SchedulingResult(
        algorithm_name="FCFS",
        request_sequence=list(requests),
        service_order=list(requests),
        head_movement_path=head_movement_path,
        individual_movements=individual_movements,
        total_head_movement=total_head_movement,
        direction=None,
    )
