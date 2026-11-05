# Disk Scheduling Algorithms — Comprehensive Documentation

**Advanced Disk Scheduling Simulator**

---

## Table of Contents

- [1. FCFS — First Come, First Served](#1-fcfs--first-come-first-served)
- [2. SSTF — Shortest Seek Time First](#2-sstf--shortest-seek-time-first)
- [3. SCAN — Elevator Algorithm](#3-scan--elevator-algorithm)
- [4. C-SCAN — Circular SCAN](#4-c-scan--circular-scan)
- [5. Algorithm Comparison](#5-algorithm-comparison)
- [6. Edge Case Handling](#6-edge-case-handling)

---

## 1. FCFS — First Come, First Served

### 1.1 Description

FCFS (First Come, First Served) is the simplest disk scheduling algorithm. Requests are serviced in the exact order they arrive in the I/O request queue, with no reordering or optimization. The disk head moves directly from its current position to the next request in the queue.

### 1.2 How It Works (Step by Step)

1. Start at the initial head position.
2. Take the first request from the queue.
3. Move the head to that cylinder and service the request.
4. Take the next request from the queue.
5. Repeat until all requests are serviced.

### 1.3 Pseudocode

```
Algorithm FCFS(requests, head_position):
    INPUT:  requests — list of cylinder numbers in arrival order
            head_position — current position of the disk head
    OUTPUT: order — list of cylinders in the order they are serviced

    order ← empty list
    current ← head_position

    for each request in requests:
        order.append(request)
        current ← request

    return order
```

### 1.4 Advantages

- **Simplicity** — Easiest to implement and understand.
- **Fairness** — Every request is served in the order it arrives; no starvation.
- **Predictability** — The service order is deterministic and matches arrival order.

### 1.5 Disadvantages

- **High seek time** — No optimization of head movement; the head may zigzag wildly across the disk.
- **Poor performance** — Can result in very high total head movement compared to other algorithms.
- **Convoy effect** — A burst of requests at one end of the disk can delay requests at the other end.

### 1.6 Time Complexity

| Operation | Complexity |
|---|---|
| Service order computation | **O(N)** |
| Total head movement calculation | **O(N)** |

Where **N** is the number of requests.

### 1.7 Worked Example

**Given:**
- Request queue: `[98, 183, 37, 122, 14, 124, 65, 67]`
- Initial head position: `53`
- Disk range: `0–199`

**Service Order:** `53 → 98 → 183 → 37 → 122 → 14 → 124 → 65 → 67`

| Step | From | To | Distance |
|---|---|---|---|
| 1 | 53 | 98 | 45 |
| 2 | 98 | 183 | 85 |
| 3 | 183 | 37 | 146 |
| 4 | 37 | 122 | 85 |
| 5 | 122 | 14 | 108 |
| 6 | 14 | 124 | 110 |
| 7 | 124 | 65 | 59 |
| 8 | 65 | 67 | 2 |

**Total Head Movement:** 45 + 85 + 146 + 85 + 108 + 110 + 59 + 2 = **640 cylinders**

### 1.8 When to Use

- When the request queue is small and optimization overhead is not justified.
- When fairness (first-come, first-served order) is the top priority.
- In low-throughput systems where seek time is not a bottleneck.

---

## 2. SSTF — Shortest Seek Time First

### 2.1 Description

SSTF (Shortest Seek Time First) selects the pending request that is closest to the current head position, minimizing the seek distance at each step. When two or more requests are equidistant, the one with the lower cylinder number is chosen (tie-breaking rule).

### 2.2 How It Works (Step by Step)

1. Start at the initial head position.
2. From all pending (unserviced) requests, find the one closest to the current head position.
3. If two requests are equidistant, choose the one with the lower cylinder number.
4. Move the head to that cylinder and service the request.
5. Remove the serviced request from the pending list.
6. Repeat until all requests are serviced.

### 2.3 Pseudocode

```
Algorithm SSTF(requests, head_position):
    INPUT:  requests — list of cylinder numbers
            head_position — current position of the disk head
    OUTPUT: order — list of cylinders in the order they are serviced

    pending ← copy of requests
    order ← empty list
    current ← head_position

    while pending is not empty:
        // Find closest request
        min_distance ← infinity
        nearest ← null

        for each request in pending:
            distance ← |request - current|
            if distance < min_distance:
                min_distance ← distance
                nearest ← request
            else if distance == min_distance and request < nearest:
                nearest ← request    // tie-break: lower cylinder

        order.append(nearest)
        current ← nearest
        remove nearest from pending

    return order
```

### 2.4 Advantages

- **Lower average seek time** — Generally produces significantly less total head movement than FCFS.
- **Locally optimal** — Each individual step minimizes seek distance.

### 2.5 Disadvantages

- **Starvation** — Requests far from the head's current position may be indefinitely postponed if new closer requests keep arriving.
- **Not globally optimal** — Greedy local optimization does not guarantee the globally optimal service order.
- **Higher computation overhead** — Must search through all pending requests at each step.

### 2.6 Time Complexity

| Operation | Complexity |
|---|---|
| Service order computation | **O(N²)** |
| Total head movement calculation | **O(N)** |

Where **N** is the number of requests. The O(N²) comes from searching through the remaining requests at each step.

### 2.7 Worked Example

**Given:**
- Request queue: `[98, 183, 37, 122, 14, 124, 65, 67]`
- Initial head position: `53`
- Disk range: `0–199`

**Service Order:** `53 → 65 → 67 → 37 → 14 → 98 → 122 → 124 → 183`

| Step | From | To | Distance | Reasoning |
|---|---|---|---|---|
| 1 | 53 | 65 | 12 | Closest to 53: 65 (dist=12) vs 37 (dist=16) |
| 2 | 65 | 67 | 2 | Closest to 65: 67 (dist=2) |
| 3 | 67 | 37 | 30 | Closest to 67: 37 (dist=30) vs 98 (dist=31) |
| 4 | 37 | 14 | 23 | Closest to 37: 14 (dist=23) vs 98 (dist=61) |
| 5 | 14 | 98 | 84 | Only farther requests remain; 98 is closest |
| 6 | 98 | 122 | 24 | Closest to 98: 122 (dist=24) |
| 7 | 122 | 124 | 2 | Closest to 122: 124 (dist=2) |
| 8 | 124 | 183 | 59 | Only 183 remains |

**Total Head Movement:** 12 + 2 + 30 + 23 + 84 + 24 + 2 + 59 = **236 cylinders**

### 2.8 When to Use

- When minimizing average seek time is the primary goal.
- In batch processing environments where the full request queue is known in advance.
- When starvation is not a concern (or when combined with aging mechanisms).

---

## 3. SCAN — Elevator Algorithm

### 3.1 Description

SCAN (also known as the Elevator Algorithm) moves the disk head in one direction, servicing all requests along the way, until it reaches the disk boundary. It then reverses direction and services the remaining requests on the return trip. The head always travels to the boundary before reversing, even if there are no more requests in that direction.

### 3.2 How It Works (Step by Step)

1. Start at the initial head position with a given direction (left or right).
2. Move the head in the current direction.
3. Service any requests encountered along the way, in order.
4. When the head reaches the disk boundary (cylinder 0 or disk_size - 1), reverse direction.
5. Continue servicing requests in the new direction.
6. Stop when all requests have been serviced.

### 3.3 Pseudocode

```
Algorithm SCAN(requests, head_position, direction, disk_size):
    INPUT:  requests — list of cylinder numbers
            head_position — current position of the disk head
            direction — "left" or "right"
            disk_size — total number of cylinders
    OUTPUT: order — list of cylinders in the order they are serviced

    left_requests ← sorted requests < head_position (descending)
    right_requests ← sorted requests > head_position (ascending)
    // Requests equal to head_position are placed based on direction
    order ← empty list

    if direction == "right":
        // Go right first
        for each request in right_requests:
            order.append(request)
        // Touch right boundary if there were right requests or at boundary
        if right_requests is not empty or head_position < disk_size - 1:
            // Head reaches disk_size - 1 (boundary counted in movement)
        // Reverse: go left
        for each request in left_requests:
            order.append(request)

    else:  // direction == "left"
        // Go left first
        for each request in left_requests:
            order.append(request)
        // Touch left boundary (cylinder 0)
        // Reverse: go right
        for each request in right_requests:
            order.append(request)

    return order
```

### 3.4 Advantages

- **No starvation** — Every request is guaranteed to be serviced within two full sweeps of the disk.
- **Uniform wait time** — Provides more uniform waiting times compared to SSTF.
- **Efficient** — Generally produces lower total head movement than FCFS.
- **Predictable** — The head movement pattern is predictable, like an elevator.

### 3.5 Disadvantages

- **Boundary traversal** — The head always travels to the disk boundary, even if no requests exist beyond the last request in that direction (unlike LOOK).
- **Bias toward middle** — Cylinders in the middle of the disk are visited more frequently than those at the edges.
- **Unnecessary movement** — Going to the boundary when no requests exist there wastes seek time.

### 3.6 Time Complexity

| Operation | Complexity |
|---|---|
| Service order computation | **O(N log N)** |
| Total head movement calculation | **O(N)** |

Where **N** is the number of requests. The O(N log N) comes from sorting the requests.

### 3.7 Worked Example

**Given:**
- Request queue: `[98, 183, 37, 122, 14, 124, 65, 67]`
- Initial head position: `53`
- Direction: `right` (moving toward higher cylinders)
- Disk range: `0–199`

**Partition:**
- Requests to the right of 53: `[65, 67, 98, 122, 124, 183]` (ascending)
- Requests to the left of 53: `[37, 14]` (descending, serviced after reversal)

**Service Order:** `53 → 65 → 67 → 98 → 122 → 124 → 183 → [199] → 37 → 14`

*(The head reaches boundary 199 before reversing, even though 183 is the last request on the right.)*

| Step | From | To | Distance |
|---|---|---|---|
| 1 | 53 | 65 | 12 |
| 2 | 65 | 67 | 2 |
| 3 | 67 | 98 | 31 |
| 4 | 98 | 122 | 24 |
| 5 | 122 | 124 | 2 |
| 6 | 124 | 183 | 59 |
| 7 | 183 | 199 | 16 |
| 8 | 199 | 37 | 162 |
| 9 | 37 | 14 | 23 |

**Total Head Movement:** 12 + 2 + 31 + 24 + 2 + 59 + 16 + 162 + 23 = **331 cylinders**

### 3.8 When to Use

- When a guarantee against starvation is required.
- In systems with heavy and uniform disk loads.
- When predictable head movement patterns are desirable.

---

## 4. C-SCAN — Circular SCAN

### 4.1 Description

C-SCAN (Circular SCAN) is a variant of SCAN that treats the disk as a circular structure. The head moves in only one direction (typically toward higher cylinders), servicing requests along the way. Upon reaching the maximum boundary, the head jumps directly to the minimum boundary (cylinder 0) without servicing any requests during the return trip, then continues in the same direction.

### 4.2 How It Works (Step by Step)

1. Start at the initial head position, moving toward higher cylinders.
2. Service all requests in ascending order from the current position to the maximum boundary.
3. When the head reaches the maximum boundary (disk_size - 1), jump to the minimum boundary (cylinder 0).
4. Continue servicing remaining requests in ascending order from cylinder 0.
5. Stop when all requests have been serviced.

### 4.3 Pseudocode

```
Algorithm C-SCAN(requests, head_position, disk_size):
    INPUT:  requests — list of cylinder numbers
            head_position — current position of the disk head
            disk_size — total number of cylinders
    OUTPUT: order — list of cylinders in the order they are serviced

    right_requests ← sorted requests >= head_position (ascending)
    left_requests ← sorted requests < head_position (ascending)
    order ← empty list

    // Service requests to the right
    for each request in right_requests:
        order.append(request)

    // Head reaches disk_size - 1, then wraps to 0
    // (boundary-to-boundary movement counted in total movement)

    // Service requests to the left (in ascending order from 0)
    for each request in left_requests:
        order.append(request)

    return order
```

### 4.4 Advantages

- **Uniform wait time** — Provides the most uniform wait times of all four algorithms because it treats the disk as circular.
- **No starvation** — Every request is guaranteed to be serviced within one full circular sweep.
- **Fair** — Unlike SCAN, cylinders near the edges don't experience longer delays.

### 4.5 Disadvantages

- **Higher total head movement** — The wrap-around from max to min boundary adds significant distance.
- **Unnecessary boundary traversal** — Like SCAN, the head goes to the boundaries even if no requests exist there.
- **Wasted return sweep** — The return trip from max to min boundary services no requests.

### 4.6 Time Complexity

| Operation | Complexity |
|---|---|
| Service order computation | **O(N log N)** |
| Total head movement calculation | **O(N)** |

Where **N** is the number of requests.

### 4.7 Worked Example

**Given:**
- Request queue: `[98, 183, 37, 122, 14, 124, 65, 67]`
- Initial head position: `53`
- Disk range: `0–199`

**Partition:**
- Requests ≥ 53: `[65, 67, 98, 122, 124, 183]` (ascending)
- Requests < 53: `[14, 37]` (ascending, serviced after wrap-around)

**Service Order:** `53 → 65 → 67 → 98 → 122 → 124 → 183 → [199] → [0] → 14 → 37`

*(The head goes to boundary 199, wraps to 0, then continues ascending.)*

| Step | From | To | Distance |
|---|---|---|---|
| 1 | 53 | 65 | 12 |
| 2 | 65 | 67 | 2 |
| 3 | 67 | 98 | 31 |
| 4 | 98 | 122 | 24 |
| 5 | 122 | 124 | 2 |
| 6 | 124 | 183 | 59 |
| 7 | 183 | 199 | 16 |
| 8 | 199 | 0 | 199 |
| 9 | 0 | 14 | 14 |
| 10 | 14 | 37 | 23 |

**Total Head Movement:** 12 + 2 + 31 + 24 + 2 + 59 + 16 + 199 + 14 + 23 = **382 cylinders**

### 4.8 When to Use

- When uniform response times for all requests are critical.
- In time-sharing systems where fairness across all users is important.
- When the workload is uniformly distributed across the disk.

---

## 5. Algorithm Comparison

### 5.1 Comparison Table

| Feature | FCFS | SSTF | SCAN | C-SCAN |
|---|---|---|---|---|
| **Service Order** | Arrival order | Closest request | Directional sweep | One-direction circular |
| **Starvation** | No | Yes (possible) | No | No |
| **Total Head Movement** | Highest | Lowest (typically) | Moderate | Moderate–High |
| **Uniform Wait Time** | No | No | Partially | Yes |
| **Implementation Complexity** | Very simple | Moderate | Moderate | Moderate |
| **Time Complexity** | O(N) | O(N²) | O(N log N) | O(N log N) |
| **Boundary Traversal** | No | No | Yes | Yes (+ wrap) |
| **Best Use Case** | Small queues, fairness | Minimum seek time | Heavy loads | Time-sharing systems |

### 5.2 Performance Comparison (Worked Example)

Using the common example: requests `[98, 183, 37, 122, 14, 124, 65, 67]`, head at `53`, disk `0–199`:

| Algorithm | Total Head Movement | Rank |
|---|---|---|
| FCFS | 640 | 4th (worst) |
| SSTF | 236 | 1st (best) |
| SCAN (right) | 331 | 2nd |
| C-SCAN | 382 | 3rd |

---

## 6. Edge Case Handling

The simulator handles the following edge cases gracefully:

### 6.1 Empty Request Queue

- **Behavior:** Returns an empty service order with zero total head movement.
- **Rationale:** No requests to service means no head movement.

### 6.2 Single Request

- **Behavior:** All algorithms produce identical results — move directly to the single request.
- **Rationale:** With only one request, there is no optimization to be done.

### 6.3 Duplicate Requests

- **Behavior:** Duplicate cylinder numbers are serviced individually in sequence. Each occurrence counts as a separate request.
- **Rationale:** Multiple I/O operations may target the same cylinder.

### 6.4 Boundary Requests (Cylinder 0 or disk_size - 1)

- **Behavior:** Requests at the boundaries are handled correctly. SCAN and C-SCAN do not double-count boundary visits.
- **Rationale:** Boundary cylinders are valid request targets.

### 6.5 Head at Boundary

- **Behavior:** If the head starts at cylinder 0 or disk_size - 1, algorithms adjust accordingly (e.g., SCAN immediately reverses if already at the boundary in that direction).
- **Rationale:** The initial head position may be at any valid cylinder.

### 6.6 All Requests on One Side

- **Behavior:** If all requests are to the left or right of the head, SCAN and C-SCAN handle this correctly by traversing to the boundary and processing all requests without unnecessary reversal overhead.
- **Rationale:** The algorithms must work correctly regardless of request distribution.

### 6.7 Head Position in Request Queue

- **Behavior:** If the initial head position coincides with a request cylinder, that request is serviced first (distance = 0).
- **Rationale:** The head is already at the requested cylinder.

### 6.8 Requests Equal to Head Position

- **Behavior:** Treated as zero-distance requests and serviced immediately.
- **Rationale:** No seek is required.

