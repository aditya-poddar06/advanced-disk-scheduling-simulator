"""Performance metrics computation for disk scheduling results.

This module provides functions to compute various performance metrics
from a SchedulingResult, including head movement statistics, seek times,
and throughput. It also supports generating step-by-step execution
tables for detailed analysis and visualization.
"""

from algorithms.common import SchedulingResult


def calculate_total_head_movement(result: SchedulingResult) -> int:
    """Return the total head movement from a scheduling result.

    This value is already pre-computed in the SchedulingResult, but this
    function serves as a verification interface and a consistent API
    entry point.

    Args:
        result: A SchedulingResult from any disk scheduling algorithm.

    Returns:
        int: Total number of cylinders traversed by the disk head.

    Examples:
        >>> from algorithms.fcfs import fcfs
        >>> result = fcfs([98, 183], 53)
        >>> calculate_total_head_movement(result)
        175
    """
    return result.total_head_movement


def calculate_average_head_movement(result: SchedulingResult) -> float:
    """Calculate the average head movement per request.

    Computed as total_head_movement / number_of_requests.

    Args:
        result: A SchedulingResult from any disk scheduling algorithm.

    Returns:
        float: Average cylinders traversed per request. Returns 0.0 if
            there are no requests in the result.

    Examples:
        >>> from algorithms.fcfs import fcfs
        >>> result = fcfs([98, 183], 53)
        >>> calculate_average_head_movement(result)
        87.5
    """
    num_requests: int = len(result.request_sequence)
    if num_requests == 0:
        return 0.0
    return result.total_head_movement / num_requests


def calculate_total_seek_time(
    result: SchedulingResult,
    seek_time_per_cylinder: float,
) -> float:
    """Calculate the total seek time for all head movements.

    Computed as total_head_movement × seek_time_per_cylinder.

    Args:
        result: A SchedulingResult from any disk scheduling algorithm.
        seek_time_per_cylinder: Time in milliseconds to traverse one
            cylinder. Must be non-negative.

    Returns:
        float: Total seek time in milliseconds.

    Examples:
        >>> from algorithms.fcfs import fcfs
        >>> result = fcfs([98, 183], 53)
        >>> calculate_total_seek_time(result, 0.1)
        17.5
    """
    return result.total_head_movement * seek_time_per_cylinder


def calculate_average_seek_time(
    result: SchedulingResult,
    seek_time_per_cylinder: float,
) -> float:
    """Calculate the average seek time per request.

    Computed as total_seek_time / number_of_requests.

    Args:
        result: A SchedulingResult from any disk scheduling algorithm.
        seek_time_per_cylinder: Time in milliseconds to traverse one
            cylinder. Must be non-negative.

    Returns:
        float: Average seek time per request in milliseconds. Returns 0.0
            if there are no requests.

    Examples:
        >>> from algorithms.fcfs import fcfs
        >>> result = fcfs([98, 183], 53)
        >>> calculate_average_seek_time(result, 0.1)
        8.75
    """
    num_requests: int = len(result.request_sequence)
    if num_requests == 0:
        return 0.0
    total_seek: float = calculate_total_seek_time(result, seek_time_per_cylinder)
    return total_seek / num_requests


def calculate_throughput(
    result: SchedulingResult,
    seek_time_per_cylinder: float,
) -> float:
    """Calculate the throughput (requests per unit time).

    Computed as number_of_requests / total_seek_time.

    Args:
        result: A SchedulingResult from any disk scheduling algorithm.
        seek_time_per_cylinder: Time in milliseconds to traverse one
            cylinder. Must be non-negative.

    Returns:
        float: Number of requests serviced per millisecond.
            Returns float('inf') if total seek time is 0 but there are
            requests (e.g., all requests are at the head position).
            Returns 0.0 if there are no requests.

    Examples:
        >>> from algorithms.fcfs import fcfs
        >>> result = fcfs([98, 183], 53)
        >>> round(calculate_throughput(result, 0.1), 4)
        0.1143
    """
    num_requests: int = len(result.request_sequence)
    if num_requests == 0:
        return 0.0
    total_seek: float = calculate_total_seek_time(result, seek_time_per_cylinder)
    if total_seek == 0:
        return float("inf")
    return num_requests / total_seek


def get_all_metrics(
    result: SchedulingResult,
    seek_time_per_cylinder: float,
) -> dict:
    """Compute all performance metrics for a single scheduling result.

    Args:
        result: A SchedulingResult from any disk scheduling algorithm.
        seek_time_per_cylinder: Time in milliseconds to traverse one
            cylinder. Must be non-negative.

    Returns:
        dict: A dictionary containing the following keys:
            - 'total_head_movement' (int): Total cylinders traversed.
            - 'average_head_movement' (float): Average cylinders per request.
            - 'total_seek_time' (float): Total seek time in ms.
            - 'average_seek_time' (float): Average seek time per request in ms.
            - 'throughput' (float): Requests per ms.

    Examples:
        >>> from algorithms.fcfs import fcfs
        >>> result = fcfs([98, 183], 53)
        >>> metrics = get_all_metrics(result, 0.1)
        >>> metrics['total_head_movement']
        175
    """
    return {
        "total_head_movement": calculate_total_head_movement(result),
        "average_head_movement": calculate_average_head_movement(result),
        "total_seek_time": calculate_total_seek_time(result, seek_time_per_cylinder),
        "average_seek_time": calculate_average_seek_time(result, seek_time_per_cylinder),
        "throughput": calculate_throughput(result, seek_time_per_cylinder),
    }


def get_step_by_step_table(result: SchedulingResult) -> list[dict]:
    """Generate a step-by-step execution table for the scheduling result.

    Each entry in the returned list represents one step of the head movement,
    showing where the head moved from, where it moved to, how far it moved,
    and the cumulative distance so far.

    For SCAN/C-SCAN, steps to boundary positions (which are not actual
    requests) are also included, giving a complete picture of the head
    trajectory.

    Args:
        result: A SchedulingResult from any disk scheduling algorithm.

    Returns:
        list[dict]: A list of dictionaries, one per step, each containing:
            - 'step' (int): Step number, starting from 1.
            - 'previous_head' (int): Head position before this step.
            - 'current_request' (int): Head position after this step
                (the cylinder the head moved to).
            - 'movement' (int): Absolute distance moved in this step.
            - 'cumulative_movement' (int): Running total of all movements
                up to and including this step.

    Examples:
        >>> from algorithms.fcfs import fcfs
        >>> result = fcfs([98, 183], 53)
        >>> table = get_step_by_step_table(result)
        >>> table[0]
        {'step': 1, 'previous_head': 53, 'current_request': 98, 'movement': 45, 'cumulative_movement': 45}
    """
    table: list[dict] = []
    cumulative: int = 0

    for i in range(len(result.head_movement_path) - 1):
        previous_head: int = result.head_movement_path[i]
        current_request: int = result.head_movement_path[i + 1]
        movement: int = result.individual_movements[i]
        cumulative += movement

        table.append(
            {
                "step": i + 1,
                "previous_head": previous_head,
                "current_request": current_request,
                "movement": movement,
                "cumulative_movement": cumulative,
            }
        )

    return table
