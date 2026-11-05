"""Disk scheduler simulation engine.

Provides the DiskSchedulerSimulator class which serves as the central
orchestration layer for running disk scheduling algorithms, collecting
results, and producing comparison data across all supported algorithms.
"""

from algorithms.common import SchedulingResult, validate_algorithm_inputs
from algorithms.fcfs import fcfs
from algorithms.sstf import sstf
from algorithms.scan import scan
from algorithms.cscan import cscan
from core.metrics import get_all_metrics


# Registry mapping algorithm names to their implementation functions
_ALGORITHM_REGISTRY: dict[str, callable] = {
    "fcfs": fcfs,
    "sstf": sstf,
    "scan": scan,
    "cscan": cscan,
}

# Algorithms that accept a direction parameter
_DIRECTIONAL_ALGORITHMS: set[str] = {"scan", "cscan"}


class DiskSchedulerSimulator:
    """Central simulation engine for disk scheduling algorithms.

    Encapsulates the disk configuration (cylinder range, head position,
    request queue) and provides methods to run individual algorithms,
    run all algorithms, and produce comparative metrics.

    Attributes:
        requests: List of cylinder numbers representing I/O requests.
        initial_head: Starting cylinder position of the disk head.
        min_cylinder: Minimum valid cylinder number.
        max_cylinder: Maximum valid cylinder number.
        direction: Initial head movement direction for SCAN/C-SCAN.
        seek_time_per_cylinder: Time (in ms) to move one cylinder. Used
            for seek time calculations in metrics.

    Examples:
        >>> sim = DiskSchedulerSimulator([98, 183, 37], 53)
        >>> result = sim.run_algorithm('fcfs')
        >>> result.algorithm_name
        'FCFS'
        >>> all_results = sim.run_all_algorithms()
        >>> len(all_results)
        4
    """

    def __init__(
        self,
        requests: list[int],
        initial_head: int,
        min_cylinder: int = 0,
        max_cylinder: int = 199,
        direction: str = "left",
        seek_time_per_cylinder: float = 0.1,
    ) -> None:
        """Initialize the simulator with disk configuration and request queue.

        Args:
            requests: List of cylinder numbers for I/O requests. May contain
                duplicates; each is serviced independently.
            initial_head: Starting cylinder position of the disk head.
            min_cylinder: Minimum valid cylinder number. Defaults to 0.
            max_cylinder: Maximum valid cylinder number. Defaults to 199.
            direction: Initial head direction for directional algorithms
                ('left' or 'right'). Defaults to 'left'.
            seek_time_per_cylinder: Time in milliseconds to traverse one
                cylinder. Must be non-negative. Defaults to 0.1.

        Raises:
            ValueError: If inputs fail validation (see validate_algorithm_inputs)
                or if direction is invalid or seek_time_per_cylinder is negative.
        """
        # Validate core algorithm inputs
        validate_algorithm_inputs(requests, initial_head, min_cylinder, max_cylinder)

        if direction not in ("left", "right"):
            raise ValueError(
                f"direction must be 'left' or 'right', got '{direction}'"
            )
        if seek_time_per_cylinder < 0:
            raise ValueError(
                f"seek_time_per_cylinder must be non-negative, "
                f"got {seek_time_per_cylinder}"
            )

        self.requests: list[int] = list(requests)
        self.initial_head: int = initial_head
        self.min_cylinder: int = min_cylinder
        self.max_cylinder: int = max_cylinder
        self.direction: str = direction
        self.seek_time_per_cylinder: float = seek_time_per_cylinder

    def run_algorithm(self, algorithm_name: str) -> SchedulingResult:
        """Run a single disk scheduling algorithm by name.

        Args:
            algorithm_name: Name of the algorithm to run. Must be one of
                'fcfs', 'sstf', 'scan', 'cscan' (case-insensitive).

        Returns:
            SchedulingResult: The complete result of the algorithm execution.

        Raises:
            ValueError: If algorithm_name is not recognized.
        """
        name_lower: str = algorithm_name.lower()

        if name_lower not in _ALGORITHM_REGISTRY:
            raise ValueError(
                f"Unknown algorithm '{algorithm_name}'. "
                f"Supported: {', '.join(sorted(_ALGORITHM_REGISTRY.keys()))}"
            )

        algo_func = _ALGORITHM_REGISTRY[name_lower]

        if name_lower in _DIRECTIONAL_ALGORITHMS:
            return algo_func(
                self.requests,
                self.initial_head,
                self.min_cylinder,
                self.max_cylinder,
                self.direction,
            )
        else:
            return algo_func(
                self.requests,
                self.initial_head,
                self.min_cylinder,
                self.max_cylinder,
            )

    def run_all_algorithms(self) -> dict[str, SchedulingResult]:
        """Run all supported disk scheduling algorithms.

        Returns:
            dict[str, SchedulingResult]: A dictionary mapping algorithm names
                (lowercase) to their SchedulingResult objects.

        Examples:
            >>> sim = DiskSchedulerSimulator([98, 183], 53)
            >>> results = sim.run_all_algorithms()
            >>> sorted(results.keys())
            ['cscan', 'fcfs', 'scan', 'sstf']
        """
        results: dict[str, SchedulingResult] = {}
        for name in _ALGORITHM_REGISTRY:
            results[name] = self.run_algorithm(name)
        return results

    def get_comparison_data(self) -> list[dict]:
        """Run all algorithms and return comparative metrics for each.

        Produces a list of dictionaries, one per algorithm, containing
        the algorithm name and all computed performance metrics.

        Returns:
            list[dict]: Each dict contains:
                - 'algorithm': Algorithm name from SchedulingResult
                - All keys from get_all_metrics (total_head_movement,
                  average_head_movement, total_seek_time,
                  average_seek_time, throughput)

        Examples:
            >>> sim = DiskSchedulerSimulator([98, 183], 53)
            >>> data = sim.get_comparison_data()
            >>> len(data)
            4
            >>> all('algorithm' in d for d in data)
            True
        """
        all_results: dict[str, SchedulingResult] = self.run_all_algorithms()
        comparison: list[dict] = []

        for _name, result in all_results.items():
            metrics: dict = get_all_metrics(result, self.seek_time_per_cylinder)
            metrics["algorithm"] = result.algorithm_name
            comparison.append(metrics)

        return comparison
