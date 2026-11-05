# Viva Preparation Guide

**CSE316 — Operating Systems | Continuous Assessment 3**  
*Comprehensive Q&A Guide for Lab Viva & Project Defense*

---

## 1. Fundamentals of Disk Storage Architecture

### Q1: What are the components of disk access time?
**Answer:**
Disk access time consists of three primary components:
1. **Seek Time:** The time required to physically move the read/write disk arm to the specified cylinder/track. This is the slowest, mechanical step and typically dominates access latency (approx. 3–15 ms).
2. **Rotational Latency:** The time taken for the desired sector on the platter to rotate beneath the read/write head. Average rotational latency is half the time for one full revolution:
   $$\text{Avg Latency} = \frac{1}{2} \times \frac{60}{\text{RPM}} \text{ seconds}$$
3. **Transfer Time:** The time taken to stream the data off the magnetic media to the disk controller buffer:
   $$\text{Transfer Time} = \frac{\text{Bytes to Transfer}}{\text{Data Transfer Rate}}$$

### Q2: Why is disk scheduling necessary?
**Answer:**
Because seek time is constrained by mechanical movement (servomotor moving the arm assembly across physical platters), random uncoordinated requests cause extensive physical delays. Disk scheduling algorithms rearrange pending I/O requests to minimize unnecessary arm travel, increase system throughput, and reduce average response times.

### Q3: What is the physical difference between a track, cylinder, and sector?
**Answer:**
- **Track:** A circular concentric ring on a single platter surface.
- **Sector:** The smallest addressable physical storage block on a track (typically 512 bytes or 4 KB).
- **Cylinder:** The collection of identical circular tracks across all platter surfaces aligned vertically at the same radial arm position.

---

## 2. Algorithm Deep Dive & Comparisons

### Q4: Explain the FCFS algorithm. What are its pros and cons?
**Answer:**
- **Concept:** Requests are serviced in the exact sequential order they arrive in the I/O queue.
- **Pros:** Absolutely fair, trivial to implement ($O(N)$), guaranteed zero starvation.
- **Cons:** Suffers from wild head oscillations across the disk surface (the *convoy effect*), producing the highest total seek distance and poor throughput.

### Q5: What is SSTF? Why does it cause starvation?
**Answer:**
- **Concept:** At each step, SSTF selects whichever pending request has the minimum absolute seek distance $|R_i - \text{Head}|$ from the current head position.
- **Tie-Breaking Rule in Our Implementation:** If two pending requests are equidistant, our implementation chooses the lower cylinder number first.
- **Starvation Mechanism:** If new I/O requests continually arrive in the vicinity of the active head cluster, requests located on distant cylinders will be repeatedly deferred and starve indefinitely.

### Q6: How does SCAN (Elevator Algorithm) work?
**Answer:**
- **Concept:** The disk arm moves steadily in one direction (e.g., towards cylinder 0), servicing every pending request along the way. Upon reaching the physical disk boundary (cylinder 0), it reverses direction and sweeps toward the opposite boundary, servicing remaining requests.
- **Analogy:** Identical to an elevator servicing floor requests all the way to the top before changing direction downwards.
- **Why visit the boundary?** In classical SCAN, the head travels all the way to the disk edge ($0$ or $C_{\max}$) to maintain predictable, bounded wait times.

### Q7: What is C-SCAN and why was it developed over SCAN?
**Answer:**
- **Concept:** Circular SCAN moves in one direction only. When it reaches the boundary, it wraps directly to the opposite physical edge without servicing requests on the return trip, and then resumes sweeping in the original direction.
- **Motivation:** In standard SCAN, cylinders near the center of the disk are visited more frequently (twice per round trip) than cylinders near the edges. C-SCAN provides a much more **uniform waiting time distribution** across all cylinders.
- **Trade-off:** C-SCAN has a higher total head movement than SCAN due to the circular wrap jump $(|C_{\max} - C_{\min}|)$, but smaller variance in waiting times.

### Q8: What is the difference between SCAN/C-SCAN and LOOK/C-LOOK?
**Answer:**
- In **SCAN / C-SCAN**, the disk head always travels all the way to the physical boundary cylinder ($0$ or $199$).
- In **LOOK / C-LOOK**, the disk arm only travels as far as the *last pending request* in that direction before reversing or wrapping, avoiding wasted seeks to empty disk edges.

---

## 3. Quantitative Calculations & Metrics

### Q9: How is Total Head Movement calculated?
**Answer:**
$$\text{Total Movement} = \sum_{i=0}^{K-1} |P_{i+1} - P_i|$$
Where $P_0$ is the initial head position, and $P_1, \dots, P_K$ are the consecutive cylinders visited (including boundary cylinders in SCAN/C-SCAN).

### Q10: How do you compute Throughput in this simulator?
**Answer:**
$$\text{Throughput} = \frac{N}{\text{Total Seek Time}} \quad (\text{requests serviced per millisecond})$$
Where $\text{Total Seek Time} = \text{Total Head Movement} \times \text{Seek Time per Cylinder (ms)}$.
If total seek time is 0 (e.g. all requests are already at the initial head position), throughput evaluates to $\infty$.

### Q11: Walk through the textbook example:
- Requests: `[98, 183, 37, 122, 14, 124, 65, 67]`
- Head: `53`, Disk: `0-199`, Direction: `left`

**Calculations:**
- **FCFS:**
  Path: `53 -> 98 -> 183 -> 37 -> 122 -> 14 -> 124 -> 65 -> 67`
  Movements: $45 + 85 + 146 + 85 + 108 + 110 + 59 + 2 = \mathbf{640\text{ cyl}}$
- **SSTF:**
  Path: `53 -> 65 -> 67 -> 37 -> 14 -> 98 -> 122 -> 124 -> 183`
  Movements: $12 + 2 + 30 + 23 + 84 + 24 + 2 + 59 = \mathbf{236\text{ cyl}}$
- **SCAN (left):**
  Path: `53 -> 37 -> 14 -> 0 -> 65 -> 67 -> 98 -> 122 -> 124 -> 183`
  Movements: $16 + 23 + 14 + 65 + 2 + 31 + 24 + 2 + 59 = \mathbf{236\text{ cyl}}$
- **C-SCAN (left):**
  Path: `53 -> 37 -> 14 -> 0 -> 199 -> 183 -> 124 -> 122 -> 98 -> 67 -> 65`
  Movements: $16 + 23 + 14 + 199 + 16 + 59 + 2 + 24 + 31 + 2 = \mathbf{382\text{ cyl}}$

---

## 4. Software Architecture & Implementation Questions

### Q12: Explain the architecture of your project.
**Answer:**
The project uses a clean **4-layer architecture**:
1. **Presentation Layer (`app.py`, `components/`):** Streamlit web UI and Plotly chart/table renderers.
2. **Orchestration Layer (`core/simulator.py`):** `DiskSchedulerSimulator` coordinates algorithm execution and aggregates comparative results.
3. **Computation Layer (`algorithms/`, `core/metrics.py`):** Pure deterministic functions returning immutable `SchedulingResult` dataclasses and calculating metrics.
4. **Validation Layer (`core/validation.py`):** Parses string inputs and aggregates all validation errors before computation.

### Q13: How did you verify the correctness of your implementation?
**Answer:**
We wrote an automated test suite with **120 tests** using `pytest`:
- Unit tests verifying every algorithm's path and movement against manual mathematical calculations.
- Validation tests covering negative inputs, inverted disk bounds, and malformed strings.
- Edge case tests covering empty request queues, single requests, duplicate cylinder requests, and boundary positions ($0$ and $199$).
- Component tests verifying Plotly trace construction and pandas DataFrame schemas.

---

## 5. Rapid-Fire Cheat Sheet

| Question | Quick Answer |
|---|---|
| Which algorithm is optimal for seek time? | SSTF (locally greedy) / SCAN (bounded global) |
| Which algorithm never starves? | FCFS, SCAN, C-SCAN |
| Which algorithm gives the most uniform wait time? | C-SCAN |
| Time complexity of FCFS? | $O(N)$ |
| Time complexity of SSTF? | $O(N^2)$ (or $O(N \log N)$ with balanced trees) |
| Time complexity of SCAN / C-SCAN? | $O(N \log N)$ (sorting left/right partitions) |
| Is circular wrap in C-SCAN counted in seek distance? | Yes, physical arm movement is required. |
| In our SSTF, how are equidistant requests resolved? | Lower cylinder number is serviced first. |
