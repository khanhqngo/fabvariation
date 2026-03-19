"""
=== app.py ===

FabVariation - Real-Time Process Variation Simulator & Excursion Preventer

This is the main Streamlit application file that provides a complete web-based
Statistical Process Control (SPC) tool for semiconductor manufacturing.

Features:
- Interactive process simulation with realistic drift scenarios
- Real-time control chart generation (X-bar, Individuals, EWMA, CUSUM)
- Western Electric and Nelson rules violation detection
- Scrap cost calculation
- Email alert simulation
- Professional PDF report generation
- CSV data export

Author: Elite Streamlit Senior Engineer
Target Users: Micron Fab SPC Coordinators and Process Engineers
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import io

# Import custom modules
from models.simulation_data import SimulationData
from utils.constants import (
    COLORS, PROCESS_PRESETS, DRIFT_SCENARIOS, CHART_TYPES,
    DEFECT_TYPES, UI_CONFIG, EWMA_DEFAULTS, CUSUM_DEFAULTS
)
from utils.calculations import SPCCalculator
from utils.chart_utils import ChartBuilder
from utils.pdf_generator import PDFReportGenerator
from utils.csv_exporter import CSVExporter


# ========== PAGE CONFIGURATION ==========
st.set_page_config(
    page_title=UI_CONFIG['page_title'],
    page_icon=UI_CONFIG['page_icon'],
    layout=UI_CONFIG['layout'],
    initial_sidebar_state=UI_CONFIG['initial_sidebar_state'],
)


# ========== CUSTOM CSS STYLING ==========
def apply_custom_css():
    """Apply custom CSS for dark theme and professional styling."""
    st.markdown(f"""
        <style>
        /* Main app background */
        .stApp {{
            background-color: {COLORS['background_dark']};
        }}

        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: {COLORS['card_background']};
        }}

        /* Metric cards */
        [data-testid="stMetricValue"] {{
            font-size: 2rem;
            color: {COLORS['primary_green']};
        }}

        /* Headers */
        h1, h2, h3 {{
            color: {COLORS['text_primary']};
        }}

        /* Buttons */
        .stButton > button {{
            background-color: {COLORS['primary_green']};
            color: white;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
        }}

        .stButton > button:hover {{
            background-color: {COLORS['primary_orange']};
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 204, 102, 0.3);
        }}

        /* Slider labels */
        .stSlider > label {{
            font-size: 1rem;
            font-weight: 600;
            color: {COLORS['text_primary']};
        }}

        /* Select boxes */
        .stSelectbox > label {{
            font-size: 1rem;
            font-weight: 600;
            color: {COLORS['text_primary']};
        }}

        /* Cards/containers */
        .css-1r6slb0 {{
            background-color: {COLORS['card_background']};
            border-radius: 10px;
            padding: 1.5rem;
        }}

        /* Alert boxes */
        .stAlert {{
            border-radius: 8px;
        }}

        /* Tables */
        .dataframe {{
            font-size: 0.9rem;
        }}

        /* Expander */
        .streamlit-expanderHeader {{
            background-color: {COLORS['card_background']};
            border-radius: 8px;
        }}
        </style>
    """, unsafe_allow_html=True)


# ========== SESSION STATE INITIALIZATION ==========
def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'simulation_data' not in st.session_state:
        st.session_state.simulation_data = None

    if 'current_dataframe' not in st.session_state:
        st.session_state.current_dataframe = None

    if 'violations' not in st.session_state:
        st.session_state.violations = []

    if 'alert_shown' not in st.session_state:
        st.session_state.alert_shown = False

    if 'simulation_history' not in st.session_state:
        st.session_state.simulation_history = []


# ========== MAIN APPLICATION ==========
def main():
    """Main application function."""

    # Apply styling
    apply_custom_css()

    # Initialize session state
    initialize_session_state()

    # App header
    st.markdown(f"""
        <h1 style='text-align: center; color: {COLORS['primary_green']}; margin-bottom: 0;'>
            FabVariation
        </h1>
        <p style='text-align: center; color: {COLORS['text_secondary']}; font-size: 1.2rem;'>
            Real-Time Process Variation Simulator & Excursion Preventer
        </p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ========== SIDEBAR CONFIGURATION ==========
    with st.sidebar:
        st.markdown(f"<h2 style='color: {COLORS['primary_orange']}'>Configuration</h2>",
                    unsafe_allow_html=True)

        # Process selection
        st.markdown("### Process Selection")
        selected_process = st.selectbox(
            "Select Process Type",
            options=list(PROCESS_PRESETS.keys()),
            index=0,
        )

        process_config = PROCESS_PRESETS[selected_process]

        # Display process info
        st.info(f"**{process_config['description']}**\n\n"
                f"Unit: {process_config['unit']}\n\n"
                f"Wafer Cost: ${process_config['wafer_cost']}")

        st.markdown("---")

        # Simulation parameters
        st.markdown("### Simulation Parameters")

        num_batches = st.slider(
            "Number of Batches",
            min_value=10,
            max_value=100,
            value=30,
            step=5,
        )

        sample_size = st.slider(
            "Sample Size per Batch",
            min_value=2,
            max_value=10,
            value=5,
            step=1,
        )

        mean_shift = st.slider(
            f"Mean Shift ({process_config['unit']})",
            min_value=-20.0,
            max_value=20.0,
            value=0.0,
            step=1.0,
        )

        sigma_multiplier = st.slider(
            "Sigma Multiplier",
            min_value=0.5,
            max_value=3.0,
            value=1.0,
            step=0.1,
        )

        st.markdown("---")

        # Drift scenario
        st.markdown("### Drift Scenario")

        drift_scenario = st.selectbox(
            "Select Drift Pattern",
            options=list(DRIFT_SCENARIOS.keys()),
            format_func=lambda x: f"{DRIFT_SCENARIOS[x]['icon']} {DRIFT_SCENARIOS[x]['name']}",
            index=0,
        )

        st.caption(DRIFT_SCENARIOS[drift_scenario]['description'])

        st.markdown("---")

        # Chart type selection
        st.markdown("### Chart Type")

        chart_type = st.selectbox(
            "Select Control Chart",
            options=list(CHART_TYPES.keys()),
            format_func=lambda x: CHART_TYPES[x]['name'],
            index=0,
        )

        st.caption(CHART_TYPES[chart_type]['best_for'])

        st.markdown("---")

        # Advanced parameters (EWMA/CUSUM)
        with st.expander("Advanced Parameters"):
            st.markdown("**EWMA Settings**")
            ewma_lambda = st.slider(
                "Lambda (λ)",
                min_value=0.05,
                max_value=0.30,
                value=EWMA_DEFAULTS['lambda'],
                step=0.05,
            )

            st.markdown("**CUSUM Settings**")
            cusum_k = st.slider(
                "Reference Value (k)",
                min_value=0.1,
                max_value=1.0,
                value=CUSUM_DEFAULTS['k'],
                step=0.1,
            )

            cusum_h = st.slider(
                "Decision Interval (h)",
                min_value=3.0,
                max_value=8.0,
                value=CUSUM_DEFAULTS['h'],
                step=0.5,
            )

    # ========== MAIN CONTENT AREA ==========

    # Action buttons row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🔄 Refresh Chart", use_container_width=True):
            generate_simulation(
                selected_process, process_config, num_batches,
                sample_size, mean_shift, sigma_multiplier, drift_scenario
            )

    with col2:
        if st.button("⚠️ Inject Defect", use_container_width=True):
            inject_defect_action()

    with col3:
        if st.button("💾 Save Log", use_container_width=True):
            save_simulation_log()

    with col4:
        if st.button("📄 Export PDF", use_container_width=True):
            export_pdf_report(
                selected_process, process_config, chart_type,
                ewma_lambda, cusum_k, cusum_h
            )

    st.markdown("---")

    # Load or generate initial data
    if st.session_state.simulation_data is None:
        with st.spinner("Loading initial simulation..."):
            generate_simulation(
                selected_process, process_config, num_batches,
                sample_size, mean_shift, sigma_multiplier, drift_scenario
            )

    # Display simulation if data exists
    if st.session_state.current_dataframe is not None:
        display_simulation_results(
            selected_process, process_config, chart_type,
            sample_size, ewma_lambda, cusum_k, cusum_h
        )

    # Display email alert if violations detected
    if st.session_state.violations and st.session_state.alert_shown:
        display_email_alert()
        st.session_state.alert_shown = False


# ========== SIMULATION FUNCTIONS ==========
def generate_simulation(
    process_name: str,
    process_config: dict,
    num_batches: int,
    sample_size: int,
    mean_shift: float,
    sigma_multiplier: float,
    drift_scenario: str
):
    """Generate new simulation data."""

    # Create simulation data object
    sim_data = SimulationData(
        process_name=process_name,
        process_unit=process_config['unit'],
        target_mean=process_config['target_mean'],
        target_sigma=process_config['target_sigma'],
        sample_size=sample_size
    )

    # Generate data
    df = sim_data.generate_data(
        num_batches=num_batches,
        mean_shift=mean_shift,
        sigma_multiplier=sigma_multiplier,
        drift_scenario=drift_scenario
    )

    # Store in session state
    st.session_state.simulation_data = sim_data
    st.session_state.current_dataframe = df

    # Calculate violations
    calculate_violations(sample_size)

    # Add to history
    st.session_state.simulation_history.append({
        'timestamp': datetime.now(),
        'process': process_name,
        'drift_scenario': drift_scenario,
        'num_violations': len(st.session_state.violations),
    })

    # Show alert if violations detected
    if st.session_state.violations:
        st.session_state.alert_shown = True


def calculate_violations(sample_size: int):
    """Calculate control chart violations."""
    df = st.session_state.current_dataframe
    sim_data = st.session_state.simulation_data

    if df is None or df.empty:
        st.session_state.violations = []
        return

    # Create calculator
    calculator = SPCCalculator(
        target_mean=sim_data.target_mean,
        target_sigma=sim_data.target_sigma
    )

    # Calculate control limits
    limits = calculator.calculate_xbar_limits(df, sample_size)

    # Detect violations
    we_violations = calculator.detect_western_electric_violations(df, limits)
    nelson_violations = calculator.detect_nelson_violations(df, limits)

    # Combine and deduplicate
    all_violations = we_violations + nelson_violations

    # Remove duplicates (same batch + rule)
    unique_violations = []
    seen = set()
    for v in all_violations:
        key = (v['batch'], v['rule'])
        if key not in seen:
            unique_violations.append(v)
            seen.add(key)

    st.session_state.violations = sorted(unique_violations, key=lambda x: x['batch'])


def inject_defect_action():
    """Inject a defect into the current simulation."""
    if st.session_state.simulation_data is None:
        st.warning("Please generate a simulation first.")
        return

    # Inject outlier
    st.session_state.simulation_data.inject_defect(
        defect_type='outlier',
        severity=5.0
    )

    # Update dataframe
    st.session_state.current_dataframe = st.session_state.simulation_data.to_dataframe()

    # Recalculate violations
    sample_size = st.session_state.simulation_data.sample_size
    calculate_violations(sample_size)

    st.success("Defect injected! Chart updated.")
    st.session_state.alert_shown = True


# ========== DISPLAY FUNCTIONS ==========
def display_simulation_results(
    process_name: str,
    process_config: dict,
    chart_type: str,
    sample_size: int,
    ewma_lambda: float,
    cusum_k: float,
    cusum_h: float
):
    """Display simulation results including charts and metrics."""

    df = st.session_state.current_dataframe
    sim_data = st.session_state.simulation_data

    # Create calculator and chart builder
    calculator = SPCCalculator(
        target_mean=sim_data.target_mean,
        target_sigma=sim_data.target_sigma
    )

    chart_builder = ChartBuilder()

    # Calculate limits
    limits = calculator.calculate_xbar_limits(df, sample_size)

    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)

    summary_stats = sim_data.get_summary_stats()

    with col1:
        st.metric(
            "Process Mean",
            f"{summary_stats['overall_mean']:.2f}",
            delta=f"{summary_stats['overall_mean'] - sim_data.target_mean:.2f}",
        )

    with col2:
        st.metric(
            "Process Std Dev",
            f"{summary_stats['overall_std']:.2f}",
            delta=f"{summary_stats['overall_std'] - sim_data.target_sigma:.2f}",
        )

    with col3:
        num_violations = len(st.session_state.violations)
        st.metric(
            "Violations Detected",
            num_violations,
            delta="Out of Control" if num_violations > 0 else "In Control",
            delta_color="inverse",
        )

    with col4:
        scrap_cost = num_violations * process_config['wafer_cost']
        st.metric(
            "Estimated Scrap Cost",
            f"${scrap_cost:,.0f}",
        )

    st.markdown("---")

    # Main control chart
    st.markdown(f"### {CHART_TYPES[chart_type]['name']}")

    if chart_type == 'xbar':
        fig = chart_builder.create_xbar_chart(
            df, limits, st.session_state.violations,
            process_name, process_config['unit']
        )
    elif chart_type == 'individuals':
        limits_ind = calculator.calculate_individuals_limits(df)
        fig = chart_builder.create_individuals_chart(
            df, limits_ind, st.session_state.violations,
            process_name, process_config['unit']
        )
    elif chart_type == 'ewma':
        ewma_values, ewma_limits = calculator.calculate_ewma(df, ewma_lambda)
        fig = chart_builder.create_ewma_chart(
            df, ewma_values, ewma_limits,
            process_name, process_config['unit'], ewma_lambda
        )
    elif chart_type == 'cusum':
        c_plus, c_minus, cusum_limits = calculator.calculate_cusum(df, cusum_k, cusum_h)
        fig = chart_builder.create_cusum_chart(
            df, c_plus, c_minus, cusum_limits,
            process_name, process_config['unit']
        )

    st.plotly_chart(fig, use_container_width=True)

    # Violations table
    if st.session_state.violations:
        st.markdown(f"### ⚠️ Control Chart Violations ({len(st.session_state.violations)})")

        violations_df = pd.DataFrame(st.session_state.violations)
        st.dataframe(
            violations_df,
            use_container_width=True,
            hide_index=True,
        )

    # Batch statistics table (expandable)
    with st.expander("📊 View Batch Statistics Table"):
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )


def display_email_alert():
    """Display simulated email alert."""
    st.success(
        f"✉️ **Email Alert Sent to Fab SPC Coordinator**\n\n"
        f"**Subject:** Process Control Violation Detected - {st.session_state.simulation_data.process_name}\n\n"
        f"**Message:** {len(st.session_state.violations)} control chart violation(s) detected. "
        f"Immediate attention required.\n\n"
        f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )


# ========== EXPORT FUNCTIONS ==========
def save_simulation_log():
    """Save simulation log as CSV."""
    if st.session_state.current_dataframe is None:
        st.warning("No simulation data to save.")
        return

    # Create CSV in memory
    csv_buffer = io.StringIO()
    metadata = {
        'process_name': st.session_state.simulation_data.process_name,
        'drift_scenario': st.session_state.simulation_data.drift_scenario,
        'target_mean': st.session_state.simulation_data.target_mean,
        'target_sigma': st.session_state.simulation_data.target_sigma,
    }

    # Write metadata as comments
    csv_buffer.write(f"# FabVariation Simulation Export\n")
    csv_buffer.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    csv_buffer.write(f"# Process: {metadata['process_name']}\n")
    csv_buffer.write(f"# Drift Scenario: {metadata['drift_scenario']}\n")
    csv_buffer.write(f"# Target Mean: {metadata['target_mean']}\n")
    csv_buffer.write(f"# Target Sigma: {metadata['target_sigma']}\n")
    csv_buffer.write(f"#\n")

    # Write dataframe
    st.session_state.current_dataframe.to_csv(csv_buffer, index=False)

    # Download button
    st.download_button(
        label="📥 Download CSV",
        data=csv_buffer.getvalue(),
        file_name=f"fabvariation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )

    st.success("Simulation log ready for download!")


def export_pdf_report(
    process_name: str,
    process_config: dict,
    chart_type: str,
    ewma_lambda: float,
    cusum_k: float,
    cusum_h: float
):
    """Export professional PDF report."""
    if st.session_state.current_dataframe is None:
        st.warning("No simulation data to export.")
        return

    with st.spinner("Generating PDF report..."):
        # Prepare data
        df = st.session_state.current_dataframe
        sim_data = st.session_state.simulation_data

        calculator = SPCCalculator(
            target_mean=sim_data.target_mean,
            target_sigma=sim_data.target_sigma
        )

        chart_builder = ChartBuilder()

        # Generate charts
        charts = []

        # X-bar chart
        limits = calculator.calculate_xbar_limits(df, sim_data.sample_size)
        xbar_fig = chart_builder.create_xbar_chart(
            df, limits, st.session_state.violations,
            process_name, process_config['unit']
        )
        charts.append(xbar_fig)

        # EWMA chart
        ewma_values, ewma_limits = calculator.calculate_ewma(df, ewma_lambda)
        ewma_fig = chart_builder.create_ewma_chart(
            df, ewma_values, ewma_limits,
            process_name, process_config['unit'], ewma_lambda
        )
        charts.append(ewma_fig)

        # Prepare metadata
        metadata = {
            'drift_scenario': sim_data.drift_scenario,
            'target_mean': sim_data.target_mean,
            'target_sigma': sim_data.target_sigma,
            'sample_size': sim_data.sample_size,
            'num_batches': len(df),
        }

        summary_stats = sim_data.get_summary_stats()
        scrap_cost = len(st.session_state.violations) * process_config['wafer_cost']

        # Generate PDF
        pdf_generator = PDFReportGenerator()

        pdf_buffer = io.BytesIO()
        temp_pdf_path = "/tmp/fabvariation_report.pdf"

        pdf_generator.generate_report(
            filepath=temp_pdf_path,
            process_name=process_name,
            process_unit=process_config['unit'],
            chart_figures=charts,
            violations=st.session_state.violations,
            summary_stats=summary_stats,
            scrap_cost=scrap_cost,
            simulation_metadata=metadata
        )

        # Read PDF file
        with open(temp_pdf_path, 'rb') as f:
            pdf_data = f.read()

        # Download button
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_data,
            file_name=f"fabvariation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
        )

        st.success("PDF report generated successfully!")


# ========== RUN APPLICATION ==========
if __name__ == "__main__":
    main()


# ===== END OF FILE: app.py =====
# This is the main application file that runs the FabVariation Streamlit web app.
# To run: streamlit run app.py
