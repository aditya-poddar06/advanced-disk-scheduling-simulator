"""Advanced Disk Scheduling Simulator — Streamlit Web Application.

CSE316 — Operating Systems | Continuous Assessment 3
Interactive tool to visualize, analyze, and compare FCFS, SSTF, SCAN,
and C-SCAN disk scheduling algorithms.
"""

from typing import Any
import streamlit as st
import pandas as pd

from algorithms.common import SchedulingResult
from core.simulator import DiskSchedulerSimulator
from core.metrics import get_all_metrics, get_step_by_step_table
from core.validation import parse_request_string, validate_all_inputs
from components.charts import (
    create_head_movement_chart,
    create_comparison_bar_chart,
    create_multi_head_movement_chart,
)
from components.tables import (
    format_step_by_step_table,
    format_comparison_table,
    format_metrics_summary,
)

# ---------------------------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Advanced Disk Scheduling Simulator",
    page_icon="🖴",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .winner-banner {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .algo-pill {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Presets Data
# ---------------------------------------------------------------------------
PRESETS = {
    "Silberschatz Textbook (Standard)": {
        "requests": "98, 183, 37, 122, 14, 124, 65, 67",
        "head": 53,
        "min_cyl": 0,
        "max_cyl": 199,
        "direction": "left",
        "seek_time": 0.1,
    },
    "High Locality (Cluster)": {
        "requests": "45, 50, 52, 54, 55, 58, 62, 180",
        "head": 53,
        "min_cyl": 0,
        "max_cyl": 199,
        "direction": "left",
        "seek_time": 0.1,
    },
    "Bimodal (Two Ends of Disk)": {
        "requests": "5, 12, 18, 25, 175, 182, 190, 195",
        "head": 100,
        "min_cyl": 0,
        "max_cyl": 199,
        "direction": "right",
        "seek_time": 0.1,
    },
    "Sequential Access": {
        "requests": "10, 20, 30, 40, 50, 60, 70, 80",
        "head": 5,
        "min_cyl": 0,
        "max_cyl": 199,
        "direction": "right",
        "seek_time": 0.1,
    },
    "Extreme Cylinders (Edges)": {
        "requests": "0, 199, 1, 198, 2, 197",
        "head": 100,
        "min_cyl": 0,
        "max_cyl": 199,
        "direction": "left",
        "seek_time": 0.1,
    },
    "Custom Workload": {
        "requests": "98, 183, 37, 122, 14, 124, 65, 67",
        "head": 53,
        "min_cyl": 0,
        "max_cyl": 199,
        "direction": "left",
        "seek_time": 0.1,
    },
}

ALGO_DESCRIPTIONS = {
    "FCFS": {
        "full_name": "First Come, First Served",
        "summary": "Services requests strictly in order of arrival with no reordering.",
        "pros": ["Completely fair to all requests", "No starvation possible", "Simple O(N) execution"],
        "cons": ["High head movement due to wild zig-zagging", "Poor seek performance"],
        "complexity": "Time: O(N) | Space: O(N)",
        "starvation": "None (guaranteed zero starvation)",
    },
    "SSTF": {
        "full_name": "Shortest Seek Time First",
        "summary": "Greedily services the pending request closest to the current head position.",
        "pros": ["Greatly reduces average seek time", "Substantial throughput increase over FCFS"],
        "cons": ["Can cause starvation for requests located far from active clusters", "Not optimal globally"],
        "complexity": "Time: O(N²) | Space: O(N)",
        "starvation": "High risk for outer/distant tracks under heavy load",
    },
    "SCAN": {
        "full_name": "SCAN (Elevator Algorithm)",
        "summary": "Moves disk arm across cylinders in one direction servicing requests until boundary, then reverses.",
        "pros": ["Bounded wait time, prevents starvation", "Predictable elevator-like traversal pattern"],
        "cons": ["Boundary delay: cylinders just visited must wait for a full round trip", "Visits boundary track even without requests"],
        "complexity": "Time: O(N log N) | Space: O(N)",
        "starvation": "None (bounded maximum wait time)",
    },
    "C-SCAN": {
        "full_name": "Circular SCAN (C-SCAN)",
        "summary": "Services requests in one direction to the boundary, wraps around to opposite boundary without servicing, and continues in the same direction.",
        "pros": ["More uniform waiting time than standard SCAN", "Treats the disk cylinders as a circular track"],
        "cons": ["Larger total seek movement because the circular return jump is traversed", "Visits both boundaries"],
        "complexity": "Time: O(N log N) | Space: O(N)",
        "starvation": "None (uniform bounded wait time)",
    },
}


# ---------------------------------------------------------------------------
# Sidebar UI & Parameter Controls
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚙️ Configuration")

    preset_choice = st.selectbox(
        "Load Preset Workload",
        options=list(PRESETS.keys()),
        index=0,
        help="Select a standard benchmark or textbook example to populate parameters automatically.",
    )
    preset_data = PRESETS[preset_choice]

    st.markdown("---")
    st.markdown("### 💽 Disk Geometry")

    col_cyl1, col_cyl2 = st.columns(2)
    with col_cyl1:
        min_cylinder = st.number_input(
            "Min Cylinder",
            min_value=0,
            value=preset_data["min_cyl"],
            step=1,
            help="Starting boundary cylinder (typically 0).",
        )
    with col_cyl2:
        max_cylinder = st.number_input(
            "Max Cylinder",
            min_value=1,
            value=preset_data["max_cyl"],
            step=1,
            help="Ending boundary cylinder (e.g., 199 for a 200-cylinder disk).",
        )

    initial_head = st.number_input(
        "Initial Head Position",
        min_value=int(min_cylinder),
        max_value=int(max_cylinder),
        value=preset_data["head"],
        step=1,
        help="Initial cylinder where the disk arm begins.",
    )

    direction = st.radio(
        "Initial Direction (SCAN / C-SCAN)",
        options=["left", "right"],
        index=0 if preset_data["direction"] == "left" else 1,
        horizontal=True,
        help="Direction towards min (left) or max (right) cylinder.",
    )

    seek_time_per_cylinder = st.number_input(
        "Seek Time per Cylinder (ms)",
        min_value=0.0,
        value=float(preset_data["seek_time"]),
        step=0.05,
        format="%.2f",
        help="Linear time constant in milliseconds to traverse one cylinder.",
    )

    st.markdown("---")
    st.markdown("### 📋 Request Queue")

    request_input = st.text_area(
        "Request Sequence (comma or space separated)",
        value=preset_data["requests"],
        height=100,
        help="Enter cylinder numbers separated by commas or spaces. Example: 98, 183, 37, 122, 14",
    )

    st.markdown("---")
    st.markdown("### 🎯 Simulation Mode")

    sim_mode = st.radio(
        "View Mode",
        options=["Compare All Algorithms", "Single Algorithm Analysis"],
        index=0,
    )

    selected_algo = "FCFS"
    if sim_mode == "Single Algorithm Analysis":
        selected_algo = st.selectbox(
            "Select Algorithm",
            options=["FCFS", "SSTF", "SCAN", "C-SCAN"],
            index=0,
        )

# ---------------------------------------------------------------------------
# Main Header
# ---------------------------------------------------------------------------
st.markdown('<div class="main-header">🖴 Advanced Disk Scheduling Simulator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">CSE316 — Operating Systems | Continuous Assessment 3 &nbsp;•&nbsp; '
    'Analyze & Compare <b>FCFS</b>, <b>SSTF</b>, <b>SCAN</b>, and <b>C-SCAN</b> algorithms</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Input Parsing & Validation
# ---------------------------------------------------------------------------
try:
    parsed_requests = parse_request_string(request_input)
except ValueError as parse_err:
    st.error(f"⚠️ **Syntax Error in Request Sequence**: {parse_err}")
    st.stop()

is_valid, validation_errors = validate_all_inputs(
    parsed_requests,
    int(initial_head),
    int(min_cylinder),
    int(max_cylinder),
    float(seek_time_per_cylinder),
)

if not is_valid:
    st.error("⚠️ **Input Validation Failed:**")
    for err in validation_errors:
        st.markdown(f"- {err}")
    st.stop()

# ---------------------------------------------------------------------------
# Simulator Execution
# ---------------------------------------------------------------------------
simulator = DiskSchedulerSimulator(
    requests=parsed_requests,
    initial_head=int(initial_head),
    min_cylinder=int(min_cylinder),
    max_cylinder=int(max_cylinder),
    direction=direction,
    seek_time_per_cylinder=float(seek_time_per_cylinder),
)

# ---------------------------------------------------------------------------
# Mode 1: Compare All Algorithms
# ---------------------------------------------------------------------------
if sim_mode == "Compare All Algorithms":
    all_results = simulator.run_all_algorithms()
    comparison_data = simulator.get_comparison_data()

    # Determine Best Performing Algorithm (Minimum Total Head Movement)
    best_algo = min(comparison_data, key=lambda x: x["total_head_movement"])
    best_name = best_algo["algorithm"]
    best_movement = best_algo["total_head_movement"]

    # Winner Callout Banner
    st.markdown(
        f"""
        <div class="winner-banner">
            <h3 style="margin: 0; font-size: 1.3rem;">🏆 Top Performer: <b>{best_name}</b></h3>
            <p style="margin: 0.25rem 0 0 0; opacity: 0.95;">
                Achieved the minimum total head movement of <b>{best_movement} cylinders</b>
                ({best_algo['total_seek_time']:.2f} ms total seek time) on this workload.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Comparison Metrics Summary Table
    st.markdown("### 📊 Performance Summary Table")
    df_comparison = format_comparison_table(comparison_data)
    st.dataframe(df_comparison, use_container_width=True, hide_index=True)

    # Download CSV button
    csv_comp = df_comparison.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Comparison Summary (CSV)",
        data=csv_comp,
        file_name="disk_scheduling_comparison.csv",
        mime="text/csv",
    )

    st.markdown("---")

    # Interactive Comparison Charts (Bar Chart + Multi-Trace Overlay)
    col_chart1, col_chart2 = st.columns([1, 1])

    with col_chart1:
        st.markdown("### 📈 Bar Chart Comparison")
        selected_metric = st.selectbox(
            "Metric to Compare",
            options=[
                ("total_head_movement", "Total Head Movement (Cylinders)"),
                ("average_head_movement", "Average Head Movement (Cylinders/Req)"),
                ("total_seek_time", "Total Seek Time (ms)"),
                ("average_seek_time", "Average Seek Time (ms/Req)"),
                ("throughput", "Throughput (Req/ms)"),
            ],
            format_func=lambda x: x[1],
            index=0,
        )
        bar_fig = create_comparison_bar_chart(comparison_data, metric=selected_metric[0])
        st.plotly_chart(bar_fig, use_container_width=True)

    with col_chart2:
        st.markdown("### 🔀 Traversal Paths Overlay")
        overlay_fig = create_multi_head_movement_chart(
            all_results,
            min_cylinder=int(min_cylinder),
            max_cylinder=int(max_cylinder),
        )
        st.plotly_chart(overlay_fig, use_container_width=True)

    st.markdown("---")

    # Detailed Tabs for Each Algorithm
    st.markdown("### 🔍 Individual Algorithm Drilldown")
    tabs = st.tabs(["FCFS", "SSTF", "SCAN", "C-SCAN"])

    for tab, algo_key in zip(tabs, ["fcfs", "sstf", "scan", "cscan"]):
        with tab:
            algo_res = all_results[algo_key]
            algo_info = ALGO_DESCRIPTIONS.get(algo_res.algorithm_name, {})
            metrics = get_all_metrics(algo_res, float(seek_time_per_cylinder))

            # 5-column metric row
            m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
            m_col1.metric("Total Head Movement", f"{metrics['total_head_movement']} cyl")
            m_col2.metric("Avg Head Movement", f"{metrics['average_head_movement']:.2f} cyl/req")
            m_col3.metric("Total Seek Time", f"{metrics['total_seek_time']:.2f} ms")
            m_col4.metric("Avg Seek Time", f"{metrics['average_seek_time']:.2f} ms/req")
            tp = metrics["throughput"]
            tp_disp = "∞" if tp == float("inf") else f"{tp:.4f} req/ms"
            m_col5.metric("Throughput", tp_disp)

            col_sub1, col_sub2 = st.columns([3, 2])
            with col_sub1:
                single_fig = create_head_movement_chart(
                    algo_res,
                    min_cylinder=int(min_cylinder),
                    max_cylinder=int(max_cylinder),
                )
                st.plotly_chart(single_fig, use_container_width=True)

            with col_sub2:
                st.markdown("**Service Sequence Trajectory:**")
                path_str = " ➔ ".join(str(c) for c in algo_res.head_movement_path)
                st.info(f"**Path:** {path_str}")

                step_data = get_step_by_step_table(algo_res)
                step_df = format_step_by_step_table(step_data)
                st.markdown("**Step-by-Step Traversal Table:**")
                st.dataframe(step_df, use_container_width=True, hide_index=True, height=300)

                csv_steps = step_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label=f"📥 Download {algo_res.algorithm_name} Steps (CSV)",
                    data=csv_steps,
                    file_name=f"{algo_key}_steps.csv",
                    mime="text/csv",
                    key=f"dl_{algo_key}",
                )

# ---------------------------------------------------------------------------
# Mode 2: Single Algorithm Analysis
# ---------------------------------------------------------------------------
else:
    algo_key = selected_algo.lower().replace("-", "")
    result = simulator.run_algorithm(algo_key)
    metrics = get_all_metrics(result, float(seek_time_per_cylinder))
    algo_info = ALGO_DESCRIPTIONS.get(selected_algo, {})

    st.markdown(f"### 🎯 {selected_algo} ({algo_info.get('full_name', '')})")
    st.markdown(f"*{algo_info.get('summary', '')}*")

    # 5-column metric row
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Head Movement", f"{metrics['total_head_movement']} cyl")
    col2.metric("Avg Head Movement", f"{metrics['average_head_movement']:.2f} cyl/req")
    col3.metric("Total Seek Time", f"{metrics['total_seek_time']:.2f} ms")
    col4.metric("Avg Seek Time", f"{metrics['average_seek_time']:.2f} ms/req")
    tp = metrics["throughput"]
    tp_disp = "∞" if tp == float("inf") else f"{tp:.4f} req/ms"
    col5.metric("Throughput", tp_disp)

    st.markdown("---")

    col_view1, col_view2 = st.columns([3, 2])

    with col_view1:
        st.markdown("#### 📉 Head Traversal Visualization")
        fig = create_head_movement_chart(
            result,
            min_cylinder=int(min_cylinder),
            max_cylinder=int(max_cylinder),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_view2:
        st.markdown("#### 📋 Execution Breakdown")
        path_str = " ➔ ".join(str(c) for c in result.head_movement_path)
        st.info(f"**Traversal Path:**\n\n{path_str}")

        step_data = get_step_by_step_table(result)
        step_df = format_step_by_step_table(step_data)
        st.dataframe(step_df, use_container_width=True, hide_index=True, height=320)

        csv_single = step_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Step Table (CSV)",
            data=csv_single,
            file_name=f"{selected_algo.lower()}_simulation_steps.csv",
            mime="text/csv",
        )

    st.markdown("---")

    # Educational Breakdown & Complexity Details
    st.markdown("#### 🧠 Algorithm Characteristics & Theoretical Analysis")
    col_char1, col_char2 = st.columns(2)

    with col_char1:
        st.markdown("**Key Advantages:**")
        for pro in algo_info.get("pros", []):
            st.markdown(f"- ✅ {pro}")
        st.markdown(f"**Computational Complexity:** `{algo_info.get('complexity', '')}`")

    with col_char2:
        st.markdown("**Key Disadvantages:**")
        for con in algo_info.get("cons", []):
            st.markdown(f"- ⚠️ {con}")
        st.markdown(f"**Starvation Risk:** `{algo_info.get('starvation', '')}`")

# ---------------------------------------------------------------------------
# Educational Guide & Theory Reference (Collapsible)
# ---------------------------------------------------------------------------
st.markdown("---")
with st.expander("📚 Theoretical Background & Formulas (Reference Guide)"):
    st.markdown(
        """
        ### 📐 Disk Scheduling Formulas

        1. **Total Head Movement:**
           $$\\text{Total Movement} = \\sum_{i=0}^{N-1} |\\text{path}[i+1] - \\text{path}[i]|$$
           *Where $\\text{path}[0]$ is the initial head position.*

        2. **Average Head Movement:**
           $$\\text{Avg Movement} = \\frac{\\text{Total Movement}}{N}$$
           *Where $N$ is the number of I/O requests.*

        3. **Total Seek Time:**
           $$\\text{Total Seek Time} = \\text{Total Movement} \\times \\text{Seek Time per Cylinder}$$

        4. **Average Seek Time:**
           $$\\text{Avg Seek Time} = \\frac{\\text{Total Seek Time}}{N}$$

        5. **Throughput:**
           $$\\text{Throughput} = \\frac{N}{\\text{Total Seek Time}} \\quad (\\text{requests / ms})$$

        ---
        ### 🔬 Algorithm Summaries

        - **FCFS (First Come, First Served)**: Strictly processes requests in arrival order. Zero overhead, zero starvation, but can cause excessive head oscillations across the disk surface.
        - **SSTF (Shortest Seek Time First)**: Always picks the closest request to the current head position. Minimizes immediate head seek, but may cause starvation for tracks far from the current head cluster.
        - **SCAN (Elevator)**: Sweeps back and forth across the entire disk surface, servicing requests along its current direction. Reverses direction upon reaching the disk edge (0 or Max). Eliminates starvation.
        - **C-SCAN (Circular SCAN)**: Moves in a single direction, services requests until reaching the disk boundary, and then jumps directly back to the beginning boundary without servicing on the return pass. Provides more uniform wait times.
        """
    )

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #94a3b8; font-size: 0.85rem; padding: 1rem 0;">
        CSE316 — Operating Systems | Continuous Assessment 3 (Disk Scheduling Simulator)<br>
        Built with Python, Streamlit, and Plotly
    </div>
    """,
    unsafe_allow_html=True,
)

