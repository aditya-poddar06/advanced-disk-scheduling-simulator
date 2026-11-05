# Advanced Disk Scheduling Simulator

An interactive web-based simulator designed to visualize, analyze, and compare disk scheduling algorithms with comprehensive performance metrics.

---

## 📖 Overview

The **Advanced Disk Scheduling Simulator** models how operating systems manage disk arm movements to service secondary storage I/O requests. Users can configure disk geometry, initial head position, seek parameters, and custom request sequences to observe head trajectories, step-by-step movements, and comparative performance across classic disk scheduling strategies.

---

## ✨ Features

- **Interactive Visualizations:** Dynamic Plotly trajectory charts displaying head traversal across cylinders.
- **Comparative Analysis:** Side-by-side performance benchmarking across all algorithms with unified bar charts and path overlays.
- **Detailed Step Breakdown:** Step-by-step movement tables showing source cylinder, destination cylinder, seek distance, and cumulative travel.
- **Performance Metrics:** Real-time computation of Total Head Movement, Average Head Movement, Total Seek Time, Average Seek Time, and Throughput.
- **Preset Workloads:** Built-in standard benchmarks including Silberschatz textbook, clustered/locality, bimodal, sequential, and extreme boundaries.
- **Data Export:** Export step-by-step simulation results and comparison summaries to CSV.
- **Defensive Validation:** Robust input parsing and boundary checking with multi-error reporting.

---

## ⚙️ Algorithms Implemented

| Algorithm | Description | Best Suited For |
|---|---|---|
| **FCFS** (First Come, First Served) | Services requests strictly in order of arrival with no reordering. | Fair, low-overhead workloads where seek optimization is unnecessary. |
| **SSTF** (Shortest Seek Time First) | Greedily selects the pending request closest to the current head position. | Minimizing average seek time locally; prone to starvation for distant tracks. |
| **SCAN** (Elevator Algorithm) | Sweeps the disk head in one direction servicing requests to the boundary, then reverses. | Preventing starvation and providing bounded wait times. |
| **C-SCAN** (Circular SCAN) | Sweeps in one direction to the boundary, wraps to the opposite boundary, and continues. | Providing uniform waiting time distribution across all cylinders. |

---

## 🛠️ Technology Stack

- **Python 3.8+** — Core application logic and algorithm engines
- **Streamlit** — Web application framework for the interactive user interface
- **Plotly** — Interactive charting and trajectory visualization
- **Pandas** — Data formatting and tabular presentation
- **Pytest** — Automated testing framework

---

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd advanced-disk-scheduling-simulator
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   - **Linux / macOS:**
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
   - **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ How to Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Open your web browser and navigate to `http://localhost:8501`.

---

## 📋 Basic Usage

1. **Select a Workload:** Choose a preset from the sidebar or select **Custom Workload**.
2. **Configure Parameters:**
   - **Min / Max Cylinder:** Define the disk geometry bounds (e.g., 0 to 199).
   - **Initial Head Position:** Specify where the disk head starts (e.g., 53).
   - **Direction:** Set the initial arm traversal direction for SCAN/C-SCAN (`left` or `right`).
   - **Seek Time per Cylinder:** Set the linear seek constant in milliseconds (default: 0.1 ms).
   - **Request Sequence:** Enter comma- or space-separated cylinder numbers (e.g., `98, 183, 37, 122, 14, 124, 65, 67`).
3. **Choose Simulation Mode:**
   - **Compare All Algorithms:** Evaluate all four algorithms side-by-side with metric comparison bars, path overlays, and summary tables.
   - **Single Algorithm Analysis:** Inspect a specific algorithm with detailed trajectory charts, metrics, and step-by-step tables.
4. **Export Results:** Download generated step tables or comparison summaries in CSV format.

---

## 🧪 Running Automated Tests

Run the Pytest suite to verify algorithm correctness, metrics, and UI components:

```bash
pytest tests/ -v
```
