# 🖴 Advanced Disk Scheduling Simulator

**CSE316 — Operating Systems | Continuous Assessment 3**

An interactive disk scheduling simulator that visualizes and compares FCFS, SSTF, SCAN, and C-SCAN algorithms with comprehensive performance metrics.

---

## 📋 Table of Contents

- [Project Description](#project-description)
- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Scope](#scope)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Architecture](#project-architecture)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Algorithm Explanations](#algorithm-explanations)
- [Performance Metrics](#performance-metrics)
- [Screenshots](#screenshots)
- [Testing](#testing)
- [Limitations](#limitations)
- [Future Scope](#future-scope)
- [Contributors](#contributors)
- [References](#references)

---

## 📖 Project Description

The **Advanced Disk Scheduling Simulator** is a web-based interactive tool designed to simulate, visualize, and compare various disk scheduling algorithms used in operating systems. It allows users to input custom disk parameters and request sequences, then observe how different scheduling algorithms (FCFS, SSTF, SCAN, and C-SCAN) process those requests. The simulator computes detailed performance metrics including total head movement, average seek time, and throughput, and presents results through interactive charts, comparison tables, and step-by-step simulation breakdowns.

This project was developed as part of **CSE316 — Operating Systems (Continuous Assessment 3)** to provide hands-on understanding of how disk scheduling algorithms function and how their performance characteristics differ under various workloads.

---

## 🎯 Problem Statement

Design and implement a **Disk Scheduling Simulator** that simulates the following disk scheduling algorithms:

1. **FCFS (First Come, First Served)**
2. **SSTF (Shortest Seek Time First)**
3. **SCAN (Elevator Algorithm)**
4. **C-SCAN (Circular SCAN)**

The simulator should accept user-defined inputs including the request queue, initial head position, and disk size. It should compute and display performance metrics such as total head movement, average seek time, and throughput. The application must provide visual representations of head movement for each algorithm and allow side-by-side comparison of all algorithms.

---

## 🏆 Objectives

1. **Understand Disk Scheduling** — Gain a deep understanding of how disk scheduling algorithms manage I/O requests to optimize disk arm movement.
2. **Compare Algorithm Performance** — Provide a platform to compare the performance of FCFS, SSTF, SCAN, and C-SCAN under identical conditions.
3. **Visualize Head Movement** — Create interactive visualizations that illustrate the disk head's traversal path for each algorithm.
4. **Analyze Performance Metrics** — Calculate and display key metrics including total head movement, average seek time, and throughput.
5. **Handle Edge Cases** — Robustly handle edge cases such as empty request queues, single requests, duplicate requests, and boundary values.

---

## 📐 Scope

### Included

- Simulation of FCFS, SSTF, SCAN, and C-SCAN disk scheduling algorithms
- Interactive web-based user interface for parameter configuration
- Performance metric computation (total/average head movement, seek time, throughput)
- Interactive head movement visualizations using Plotly
- Side-by-side algorithm comparison mode
- Step-by-step simulation tables showing each head movement
- Input validation and error handling
- Comprehensive automated test suite

### Excluded

- LOOK and C-LOOK algorithm variants (planned for future scope)
- Rotational latency modeling
- Multi-platter and multi-head disk simulation
- Real-time disk I/O monitoring or integration with actual hardware
- Transfer time and queuing delay considerations

---

## ✨ Features

| Feature | Description |
|---|---|
| **Algorithm Simulation** | Simulate FCFS, SSTF, SCAN, and C-SCAN algorithms with configurable parameters |
| **Interactive Inputs** | Configure disk size, initial head position, direction, seek time per cylinder, and request sequence |
| **Performance Metrics** | Compute total head movement, average head movement, total seek time, average seek time, and throughput |
| **Head Movement Visualization** | Interactive Plotly charts showing the disk head's traversal path |
| **Algorithm Comparison** | Compare all four algorithms side-by-side with a unified bar chart |
| **Step-by-Step Tables** | Detailed tables showing each step of the simulation with current position, next request, and distance moved |
| **Edge Case Handling** | Graceful handling of empty queues, single requests, duplicates, and boundary conditions |
| **Input Validation** | Real-time validation with descriptive error messages |
| **Responsive Design** | Clean, responsive web interface powered by Streamlit |

---

## 🛠️ Technologies Used

| Technology | Purpose | Version |
|---|---|---|
| **Python 3** | Core programming language | 3.8+ |
| **Streamlit** | Web application framework for the interactive UI | ≥ 1.28.0 |
| **Plotly** | Interactive charting and visualization library | ≥ 5.18.0 |
| **Pytest** | Automated testing framework | ≥ 7.4.0 |
| **Git** | Version control system | — |

---

## 🏗️ Project Architecture

```
ca-cse316/
│
├── app.py                      # Main Streamlit application entry point
├── requirements.txt            # Python package dependencies
├── README.md                   # Project documentation (this file)
├── LICENSE                     # MIT License
├── .gitignore                  # Git ignore rules
│
├── algorithms/                 # Disk scheduling algorithm implementations
│   ├── __init__.py             # Package initializer
│   ├── fcfs.py                 # First Come, First Served algorithm
│   ├── sstf.py                 # Shortest Seek Time First algorithm
│   ├── scan.py                 # SCAN (Elevator) algorithm
│   └── cscan.py                # Circular SCAN algorithm
│
├── core/                       # Core application logic
│   ├── __init__.py             # Package initializer
│   ├── simulator.py            # Simulator engine (orchestrates algorithm execution)
│   ├── metrics.py              # Performance metric calculations
│   └── validation.py           # Input validation utilities
│
├── components/                 # UI components
│   ├── __init__.py             # Package initializer
│   ├── charts.py               # Plotly chart generation
│   └── tables.py               # Result table formatting
│
├── tests/                      # Automated test suite
│   ├── __init__.py             # Package initializer
│   ├── test_fcfs.py            # Tests for FCFS algorithm
│   ├── test_sstf.py            # Tests for SSTF algorithm
│   ├── test_scan.py            # Tests for SCAN algorithm
│   ├── test_cscan.py           # Tests for C-SCAN algorithm
│   ├── test_metrics.py         # Tests for metric calculations
│   └── test_validation.py      # Tests for input validation
│
└── docs/                       # Documentation
    ├── architecture.md         # System architecture documentation
    ├── algorithms.md           # Algorithm documentation
    ├── testing.md              # Testing documentation
    ├── flowchart.md            # Application flowcharts
    ├── PROJECT_REPORT.md       # Complete academic project report
    └── viva_preparation.md     # Viva preparation guide
```

### Directory Descriptions

- **`algorithms/`** — Contains self-contained implementations of each disk scheduling algorithm. Each module exposes a function that takes a request queue and parameters and returns the ordered traversal sequence.
- **`core/`** — Houses the simulator engine that coordinates algorithm execution, the metrics calculator that computes performance statistics, and the input validation module.
- **`components/`** — Contains UI helper modules for generating Plotly charts and formatting result tables for display in the Streamlit interface.
- **`tests/`** — Comprehensive test suite using Pytest with unit tests for each algorithm, metric calculations, and input validation logic.
- **`docs/`** — Project documentation including architecture details, algorithm explanations, testing strategy, flowcharts, the project report, and a viva preparation guide.

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ca-cse316
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Running the Application

```bash
streamlit run app.py
```

The application will start and open in your default web browser at `http://localhost:8501`.

### Usage

1. Configure disk parameters (disk size, initial head position, direction).
2. Enter the request sequence as comma-separated cylinder numbers.
3. Set the seek time per cylinder (in milliseconds).
4. Choose to run a single algorithm or compare all four.
5. View results including metrics, charts, and step-by-step tables.

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

To run tests with coverage report:

```bash
pytest tests/ -v --cov=algorithms --cov=core --cov-report=term-missing
```

---

## 📚 Algorithm Explanations

### FCFS — First Come, First Served

Processes disk I/O requests in the exact order they arrive in the queue. The simplest scheduling algorithm with no reordering.

```
Algorithm FCFS(requests, head_position):
    order = []
    current = head_position
    for each request in requests:
        order.append(request)
        current = request
    return order
```

**Characteristics:** Fair, no starvation, but can result in large total head movement due to no optimization.

---

### SSTF — Shortest Seek Time First

Always services the request closest to the current head position. In case of a tie, the lower cylinder number is serviced first.

```
Algorithm SSTF(requests, head_position):
    pending = copy(requests)
    order = []
    current = head_position
    while pending is not empty:
        nearest = request in pending with min |request - current|
        (break ties by choosing lower cylinder)
        order.append(nearest)
        current = nearest
        remove nearest from pending
    return order
```

**Characteristics:** Minimizes average seek time locally, but can cause starvation for distant requests.

---

### SCAN — Elevator Algorithm

The disk arm moves in one direction servicing all requests until it reaches the disk boundary, then reverses direction and services the remaining requests.

```
Algorithm SCAN(requests, head_position, direction, disk_size):
    order = []
    current = head_position
    if direction == "left":
        service requests < current in descending order
        go to cylinder 0
        service requests > current in ascending order
    else:  // direction == "right"
        service requests > current in ascending order
        go to cylinder (disk_size - 1)
        service requests < current in descending order
    return order
```

**Characteristics:** Uniform wait times, no starvation, predictable behavior similar to an elevator.

---

### C-SCAN — Circular SCAN

A variant of SCAN that only services requests in one direction. Upon reaching the disk boundary, it wraps around to the opposite boundary and continues in the same direction.

```
Algorithm C-SCAN(requests, head_position, disk_size):
    order = []
    current = head_position
    service requests > current in ascending order
    go to cylinder (disk_size - 1)
    wrap to cylinder 0
    service requests < current in ascending order
    return order
```

**Characteristics:** Provides more uniform wait times than SCAN, treats the disk as a circular structure.

---

## 📊 Performance Metrics

The simulator calculates the following performance metrics for each algorithm:

### 1. Total Head Movement

The cumulative distance traveled by the disk head across all movements.

```
Total Head Movement = Σ |position[i+1] - position[i]|    for i = 0 to N-1
```

Where `position[0]` is the initial head position and `position[1..N]` are the serviced requests in order.

### 2. Average Head Movement

The mean distance per request.

```
Average Head Movement = Total Head Movement / N
```

Where `N` is the number of requests in the queue.

### 3. Total Seek Time

The total time spent seeking, computed using a configurable seek time per cylinder.

```
Total Seek Time = Total Head Movement × Seek Time per Cylinder
```

### 4. Average Seek Time

The mean seek time per request.

```
Average Seek Time = Total Seek Time / N
```

### 5. Throughput

The number of requests serviced per unit time.

```
Throughput = N / Total Seek Time
```

---

## 📸 Screenshots

> Screenshots will be added after deployment.

---

## 🧪 Testing

The project includes a comprehensive automated test suite built with **Pytest**. Tests are organized by module and cover:

- **Algorithm Correctness** — Verifies that each algorithm produces the correct service order for known inputs.
- **Metric Calculations** — Ensures all performance metrics are computed accurately.
- **Input Validation** — Tests that invalid inputs are properly rejected with appropriate error messages.
- **Edge Cases** — Covers empty request queues, single requests, duplicate cylinder numbers, boundary values (0 and max cylinder), and all requests on one side of the head.

See [docs/testing.md](docs/testing.md) for the full testing strategy and test case documentation.

---

## ⚠️ Limitations

1. **Simplified Seek Time Model** — The simulator uses a linear seek time model (distance × constant) rather than a more realistic non-linear model that accounts for acceleration and deceleration of the disk arm.
2. **No Rotational Latency** — The simulation does not model rotational latency (the time for the desired sector to rotate under the head).
3. **Sequential Processing Only** — Requests are processed sequentially; the simulator does not model concurrent I/O or queue arrivals during processing.
4. **No Real-Time Scheduling** — The full request queue is known upfront; the simulator does not handle dynamically arriving requests.
5. **Single Disk Head** — Only a single disk head is modeled; multi-head and multi-platter configurations are not supported.

---

## 🔮 Future Scope

1. **LOOK and C-LOOK Algorithms** — Implement LOOK and C-LOOK variants that reverse direction at the last request rather than the disk boundary.
2. **Rotational Latency Modeling** — Add rotational latency simulation for more realistic seek time calculations.
3. **Multi-Platter Simulation** — Model multiple platters with independent heads.
4. **Real-Time Animation** — Animate the disk head movement step-by-step with play/pause controls.
5. **Dynamic Request Arrival** — Support requests arriving while the disk is already processing.
6. **Custom Algorithm Plugin** — Allow users to define and plug in their own scheduling algorithms.
7. **Export Reports** — Generate downloadable PDF reports of simulation results.

---

## 👥 Contributors

| Name | Enrollment Number | Email |
|---|---|---|
| Aditya | *[Enrollment Number]* | *[Email Address]* |

---

## 📚 References

1. Silberschatz, A., Galvin, P.B., and Gagne, G. **"Operating System Concepts"**, 10th Edition, Wiley, 2018. Chapter 11: Mass-Storage Structure.

2. Tanenbaum, A.S. and Bos, H. **"Modern Operating Systems"**, 4th Edition, Pearson, 2014. Chapter 5: Input/Output.

3. Stallings, W. **"Operating Systems: Internals and Design Principles"**, 9th Edition, Pearson, 2018.

4. GeeksforGeeks. **"Disk Scheduling Algorithms"**. Available at: [https://www.geeksforgeeks.org/disk-scheduling-algorithms/](https://www.geeksforgeeks.org/disk-scheduling-algorithms/)

---

<p align="center">
  <em>Developed for CSE316 — Operating Systems | Continuous Assessment 3</em>
</p>

