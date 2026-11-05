# System and Algorithm Flowcharts

**CSE316 — Operating Systems | Continuous Assessment 3**  
*Advanced Disk Scheduling Simulator*

---

## 1. System Execution Flowchart

The overall system processes user input through a pipeline of validation, simulation, metrics calculation, and interactive rendering:

```mermaid
flowchart TD
    Start(["User Launches Simulator"]) --> LoadPresets["Load Preset or Input Custom Parameters"]
    LoadPresets --> GetInputs["Input: Cylinders, Initial Head, Direction, Seek Time, Requests"]
    GetInputs --> ParseReq["Parse Request String (core/validation.py)"]
    ParseReq --> Validate{"Are All Inputs Valid?"}
    
    Validate -- "No" --> ShowErrors["Display Validation Errors in UI"]
    ShowErrors --> GetInputs
    
    Validate -- "Yes" --> CheckMode{"Simulation Mode"}
    
    CheckMode -- "Single Algorithm" --> RunSingle["Execute Selected Algorithm (algorithms/*)"]
    CheckMode -- "Compare All" --> RunAll["Execute All 4 Algorithms (FCFS, SSTF, SCAN, C-SCAN)"]
    
    RunSingle --> CalcMetricsSingle["Calculate Metrics & Step Table (core/metrics.py)"]
    RunAll --> CalcMetricsAll["Calculate Comparative Metrics & Step Tables"]
    
    CalcMetricsSingle --> RenderSingle["Render Plotly Traversal Chart, Metric Cards & Table"]
    CalcMetricsAll --> RenderAll["Render Comparison Table, Bar Chart, Overlay & Drilldowns"]
    
    RenderSingle --> DownloadOpt1["Optional: Export Steps to CSV"]
    RenderAll --> DownloadOpt2["Optional: Export Comparison & Steps to CSV"]
    
    DownloadOpt1 --> End(["User Interaction / Next Run"])
    DownloadOpt2 --> End
```

---

## 2. FCFS (First Come, First Served) Flowchart

FCFS processes requests strictly in the order they arrive in the queue.

```mermaid
flowchart TD
    A(["Start FCFS"]) --> B["Validate Inputs"]
    B --> C{"Is Request Queue Empty?"}
    C -- "Yes" --> D["Return Result with Head Position, 0 Movement"]
    C -- "No" --> E["Set current_position = initial_head"]
    E --> F["Set path = [initial_head]"]
    F --> G["For each request in request_queue"]
    G --> H["Move head directly to request"]
    H --> I["movement = |request - current_position|"]
    I --> J["Append request to path and service_order"]
    J --> K["total_movement += movement"]
    K --> L["current_position = request"]
    L --> M{"More requests in queue?"}
    M -- "Yes" --> G
    M -- "No" --> N["Return SchedulingResult"]
    N --> EndFCFS(["End FCFS"])
```

---

## 3. SSTF (Shortest Seek Time First) Flowchart

SSTF selects the pending request that requires the minimum head movement from the current head position. Ties are broken by choosing the lower cylinder number.

```mermaid
flowchart TD
    A(["Start SSTF"]) --> B["Validate Inputs"]
    B --> C{"Is Request Queue Empty?"}
    C -- "Yes" --> D["Return Result with Head Position, 0 Movement"]
    C -- "No" --> E["Initialize pending_requests = copy of requests"]
    E --> F["Set current_head = initial_head"]
    F --> G["While pending_requests is not empty"]
    G --> H["For each pending request, calculate distance = |req - current_head|"]
    H --> I["Find request with minimum distance"]
    I --> J{"Is there a distance tie?"}
    J -- "Yes" --> K["Select request with lower cylinder number"]
    J -- "No" --> L["Select closest request"]
    K --> M["Service selected request"]
    L --> M
    M --> N["movement = |selected - current_head|"]
    N --> O["Append selected to path and service_order"]
    O --> P["total_movement += movement"]
    P --> Q["Remove selected from pending_requests"]
    Q --> R["current_head = selected"]
    R --> S{"Any pending requests left?"}
    S -- "Yes" --> G
    S -- "No" --> T["Return SchedulingResult"]
    T --> EndSSTF(["End SSTF"])
```

---

## 4. SCAN (Elevator Algorithm) Flowchart

SCAN moves the head in the designated direction servicing requests until it hits the boundary, then reverses direction.

```mermaid
flowchart TD
    A(["Start SCAN"]) --> B["Validate Inputs & Direction"]
    B --> C{"Is Request Queue Empty?"}
    C -- "Yes" --> D["Return Result with Head Position, 0 Movement"]
    C -- "No" --> E["Partition requests: left_requests <= head, right_requests > head"]
    E --> F{"Initial Direction?"}
    
    F -- "left" --> G1["Sort left_requests in descending order"]
    G1 --> H1["Service left_requests toward min_cylinder"]
    H1 --> I1["Append min_cylinder to path if not already visited"]
    I1 --> J1["Reverse direction: sort right_requests in ascending order"]
    J1 --> K1["Service right_requests toward max_cylinder"]
    
    F -- "right" --> G2["Sort right_requests in ascending order"]
    G2 --> H2["Service right_requests toward max_cylinder"]
    H2 --> I2["Append max_cylinder to path if not already visited"]
    I2 --> J2["Reverse direction: sort left_requests in descending order"]
    J2 --> K2["Service left_requests toward min_cylinder"]
    
    K1 --> L["Calculate individual step movements and total head movement"]
    K2 --> L
    L --> M["Return SchedulingResult"]
    M --> EndSCAN(["End SCAN"])
```

---

## 5. C-SCAN (Circular SCAN) Flowchart

C-SCAN services requests in one direction only. When it reaches the boundary, it wraps directly to the opposite boundary and resumes servicing in the original direction.

```mermaid
flowchart TD
    A(["Start C-SCAN"]) --> B["Validate Inputs & Direction"]
    B --> C{"Is Request Queue Empty?"}
    C -- "Yes" --> D["Return Result with Head Position, 0 Movement"]
    C -- "No" --> E["Partition requests: left_requests <= head, right_requests > head"]
    E --> F{"Initial Direction?"}
    
    F -- "left" --> G1["Service left_requests in descending order"]
    G1 --> H1["Reach min_cylinder boundary"]
    H1 --> I1{"Are there right_requests pending?"}
    I1 -- "Yes" --> J1["Wrap head to max_cylinder boundary"]
    J1 --> K1["Continue servicing right_requests in descending order"]
    I1 -- "No" --> L
    
    F -- "right" --> G2["Service right_requests in ascending order"]
    G2 --> H2["Reach max_cylinder boundary"]
    H2 --> I2{"Are there left_requests pending?"}
    I2 -- "Yes" --> J2["Wrap head to min_cylinder boundary"]
    J2 --> K2["Continue servicing left_requests in ascending order"]
    I2 -- "No" --> L
    
    K1 --> L["Compute step movements: wrap traversal IS counted in total head movement"]
    K2 --> L
    L --> M["Return SchedulingResult"]
    M --> EndCSCAN(["End C-SCAN"])
```
