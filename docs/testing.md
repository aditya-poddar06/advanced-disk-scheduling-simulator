# Testing Documentation

**Advanced Disk Scheduling Simulator — Testing Strategy & Test Cases**

---

## Table of Contents

- [1. Testing Strategy](#1-testing-strategy)
- [2. Test Environment](#2-test-environment)
- [3. Test Categories](#3-test-categories)
- [4. Test Cases by Module](#4-test-cases-by-module)
- [5. How to Run Tests](#5-how-to-run-tests)
- [6. Expected Coverage](#6-expected-coverage)
- [7. Edge Cases Tested](#7-edge-cases-tested)

---

## 1. Testing Strategy

The project follows a **comprehensive testing strategy** using Pytest that covers three levels:

1. **Unit Tests** — Test individual algorithm functions and metric calculations in isolation.
2. **Integration Tests** — Test the interaction between the simulator engine, algorithms, and metrics calculator.
3. **Edge Case Tests** — Test boundary conditions, empty inputs, and unusual configurations.

All tests use a **known-answer testing** approach: expected results are manually computed for known inputs, and assertions verify that the implementation matches.

---

## 2. Test Environment

| Component | Specification |
|---|---|
| Testing framework | Pytest ≥ 7.4.0 |
| Python version | 3.8+ |
| Test location | `tests/` directory |
| Test naming | `test_<module>.py` |
| Assertion style | Standard `assert` statements |

---

## 3. Test Categories

### 3.1 Unit Tests

Test individual functions in isolation with known inputs and expected outputs.

- Each algorithm function is tested with standard request queues.
- Each metric function is tested with pre-computed values.
- Validation functions are tested with valid and invalid inputs.

### 3.2 Integration Tests

Test the full pipeline from input to result:

- Simulator engine invokes an algorithm and passes results to metrics.
- Verify that the complete result object contains correct service order and metrics.

### 3.3 Edge Case Tests

Test unusual or boundary conditions:

- Empty request queue
- Single request
- Duplicate requests
- Requests at cylinder 0 and disk_size - 1
- Head at boundary positions
- All requests on one side of the head

---

## 4. Test Cases by Module

### 4.1 FCFS Algorithm (`test_fcfs.py`)

| Test ID | Test Name | Description | Input | Expected Output |
|---|---|---|---|---|
| F01 | `test_fcfs_standard` | Standard request queue | requests=[98,183,37,122,14,124,65,67], head=53 | order=[98,183,37,122,14,124,65,67] |
| F02 | `test_fcfs_empty_queue` | Empty request queue | requests=[], head=53 | order=[] |
| F03 | `test_fcfs_single_request` | Single request | requests=[98], head=53 | order=[98] |
| F04 | `test_fcfs_duplicates` | Duplicate requests | requests=[50,50,100], head=0 | order=[50,50,100] |
| F05 | `test_fcfs_head_at_request` | Head starts at a request | requests=[53,100], head=53 | order=[53,100] |
| F06 | `test_fcfs_descending` | Requests in descending order | requests=[180,120,60,10], head=100 | order=[180,120,60,10] |
| F07 | `test_fcfs_boundary` | Requests at boundaries | requests=[0,199], head=100 | order=[0,199] |

### 4.2 SSTF Algorithm (`test_sstf.py`)

| Test ID | Test Name | Description | Input | Expected Output |
|---|---|---|---|---|
| S01 | `test_sstf_standard` | Standard request queue | requests=[98,183,37,122,14,124,65,67], head=53 | order=[65,67,37,14,98,122,124,183] |
| S02 | `test_sstf_empty_queue` | Empty request queue | requests=[], head=53 | order=[] |
| S03 | `test_sstf_single_request` | Single request | requests=[98], head=53 | order=[98] |
| S04 | `test_sstf_tie_break` | Tie-break: lower cylinder wins | requests=[40,60], head=50 | order=[40,60] (40 < 60, both dist=10) |
| S05 | `test_sstf_duplicates` | Duplicate requests | requests=[50,50], head=53 | order=[50,50] |
| S06 | `test_sstf_all_left` | All requests left of head | requests=[10,20,30], head=50 | order=[30,20,10] |
| S07 | `test_sstf_all_right` | All requests right of head | requests=[60,70,80], head=50 | order=[60,70,80] |
| S08 | `test_sstf_head_at_request` | Head at a request | requests=[53,100], head=53 | order=[53,100] |

### 4.3 SCAN Algorithm (`test_scan.py`)

| Test ID | Test Name | Description | Input | Expected Output |
|---|---|---|---|---|
| SC01 | `test_scan_right_standard` | SCAN right, standard queue | requests=[98,183,37,122,14,124,65,67], head=53, dir=right, disk=200 | order=[65,67,98,122,124,183,37,14] |
| SC02 | `test_scan_left_standard` | SCAN left, standard queue | requests=[98,183,37,122,14,124,65,67], head=53, dir=left, disk=200 | order=[37,14,65,67,98,122,124,183] |
| SC03 | `test_scan_empty_queue` | Empty request queue | requests=[], head=53, dir=right, disk=200 | order=[] |
| SC04 | `test_scan_single_request` | Single request | requests=[98], head=53, dir=right, disk=200 | order=[98] |
| SC05 | `test_scan_all_right` | All requests right of head | requests=[60,80,100], head=50, dir=right, disk=200 | order=[60,80,100] |
| SC06 | `test_scan_all_left` | All requests left of head | requests=[10,20,30], head=50, dir=right, disk=200 | order=[10,20,30] (reverse after boundary) |
| SC07 | `test_scan_head_at_boundary` | Head at cylinder 0 | requests=[50,100], head=0, dir=right, disk=200 | order=[50,100] |
| SC08 | `test_scan_boundary_requests` | Requests include boundaries | requests=[0,199,100], head=50, dir=right, disk=200 | order=[100,199,0] |

### 4.4 C-SCAN Algorithm (`test_cscan.py`)

| Test ID | Test Name | Description | Input | Expected Output |
|---|---|---|---|---|
| CS01 | `test_cscan_standard` | Standard request queue | requests=[98,183,37,122,14,124,65,67], head=53, disk=200 | order=[65,67,98,122,124,183,14,37] |
| CS02 | `test_cscan_empty_queue` | Empty request queue | requests=[], head=53, disk=200 | order=[] |
| CS03 | `test_cscan_single_request` | Single request | requests=[98], head=53, disk=200 | order=[98] |
| CS04 | `test_cscan_all_right` | All requests right of head | requests=[60,80,100], head=50, disk=200 | order=[60,80,100] |
| CS05 | `test_cscan_all_left` | All requests left of head | requests=[10,20,30], head=50, disk=200 | order=[10,20,30] (after wrap) |
| CS06 | `test_cscan_head_at_boundary` | Head at cylinder 0 | requests=[50,100,150], head=0, disk=200 | order=[50,100,150] |
| CS07 | `test_cscan_boundary_requests` | Requests include boundaries | requests=[0,199,100], head=50, disk=200 | order=[100,199,0] |
| CS08 | `test_cscan_duplicates` | Duplicate requests | requests=[50,50,100], head=0, disk=200 | order=[50,50,100] |

### 4.5 Metrics (`test_metrics.py`)

| Test ID | Test Name | Description | Expected |
|---|---|---|---|
| M01 | `test_total_head_movement` | Total head movement for known service order | Manually computed sum |
| M02 | `test_average_head_movement` | Average = Total / N | Correctly divided |
| M03 | `test_total_seek_time` | Total = Movement × Seek rate | Correctly multiplied |
| M04 | `test_average_seek_time` | Average = Total seek / N | Correctly divided |
| M05 | `test_throughput` | Throughput = N / Total seek time | Correctly computed |
| M06 | `test_metrics_single_request` | Single request metrics | Distance from head to request |
| M07 | `test_metrics_empty_request` | Empty request metrics | All zeros (or handled gracefully) |
| M08 | `test_metrics_zero_movement` | Head already at request | Movement = 0 |

### 4.6 Validation (`test_validation.py`)

| Test ID | Test Name | Description | Expected |
|---|---|---|---|
| V01 | `test_valid_inputs` | All inputs are valid | No error raised |
| V02 | `test_negative_disk_size` | Disk size < 0 | Validation error |
| V03 | `test_zero_disk_size` | Disk size = 0 | Validation error |
| V04 | `test_head_out_of_range` | Head > disk_size - 1 | Validation error |
| V05 | `test_negative_head` | Head < 0 | Validation error |
| V06 | `test_request_out_of_range` | Request > disk_size - 1 | Validation error |
| V07 | `test_negative_request` | Request < 0 | Validation error |
| V08 | `test_negative_seek_time` | Seek time ≤ 0 | Validation error |
| V09 | `test_non_integer_request` | Float in request queue | Validation error |
| V10 | `test_valid_boundary_values` | Requests at 0 and disk_size-1 | No error raised |

---

## 5. How to Run Tests

### Run all tests

```bash
pytest tests/ -v
```

### Run tests for a specific module

```bash
pytest tests/test_fcfs.py -v
pytest tests/test_sstf.py -v
pytest tests/test_scan.py -v
pytest tests/test_cscan.py -v
pytest tests/test_metrics.py -v
pytest tests/test_validation.py -v
```

### Run tests with coverage

```bash
pytest tests/ -v --cov=algorithms --cov=core --cov-report=term-missing
```

### Run a specific test

```bash
pytest tests/test_fcfs.py::test_fcfs_standard -v
```

---

## 6. Expected Coverage

| Module | Expected Coverage |
|---|---|
| `algorithms/fcfs.py` | 100% |
| `algorithms/sstf.py` | 100% |
| `algorithms/scan.py` | 100% |
| `algorithms/cscan.py` | 100% |
| `core/metrics.py` | 100% |
| `core/validation.py` | 100% |
| `core/simulator.py` | ≥ 90% |
| **Overall** | **≥ 95%** |

---

## 7. Edge Cases Tested

| Edge Case | Algorithms Tested | Expected Behavior |
|---|---|---|
| **Empty request queue** | All | Returns empty order, zero metrics |
| **Single request** | All | Direct move from head to request |
| **Duplicate requests** | All | Each duplicate serviced individually |
| **Boundary requests (0, max)** | All | Handled correctly, no out-of-range errors |
| **Head at boundary** | SCAN, C-SCAN | Correct directional behavior |
| **All requests left of head** | SSTF, SCAN, C-SCAN | Correct ordering in constrained direction |
| **All requests right of head** | SSTF, SCAN, C-SCAN | Correct ordering in constrained direction |
| **Head equals a request** | All | Zero-distance movement for that request |
| **Tie-breaking (equidistant)** | SSTF | Lower cylinder number chosen |
| **Requests in sorted order** | All | Correct handling regardless of input order |
| **Large disk with few requests** | All | Large distances computed correctly |
| **Disk size = 1** | All | Only cylinder 0 valid |

