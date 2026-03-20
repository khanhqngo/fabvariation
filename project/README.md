# FabVariation - Real-Time Process Variation Simulator & Excursion Preventer

A production-quality web application for semiconductor manufacturing Statistical Process Control (SPC), specifically designed for Micron Fab SPC Coordinators and process engineers.

## Features

- **Real-Time Process Simulation**: Simulate semiconductor processes (Plasma Etch Rate, Wafer Thickness, Deposition Rate, etc.) with realistic variation patterns
- **Multiple Drift Scenarios**: Stable process, gradual shift, sudden spike, and cyclic drift patterns
- **Advanced Control Charts**: X-bar, Individuals, EWMA, and CUSUM charts with interactive visualizations
- **Rule-Based Violation Detection**: Full implementation of Western Electric and Nelson rules
- **Defect Injection**: Test your process monitoring by injecting outliers and shifts
- **Scrap Cost Calculator**: Real-time estimation of costs from out-of-control conditions
- **Email Alerts**: Simulated email notifications to SPC coordinators
- **Professional PDF Reports**: Export comprehensive reports with charts, statistics, and violation logs
- **CSV Export**: Download raw simulation data for further analysis
- **Dark Theme UI**: Beautiful, professional interface optimized for industrial use

## Technology Stack

- **Python 3.11+**
- **Streamlit 1.42+** - Web framework
- **Pandas** - Data manipulation
- **NumPy** - Numerical computations
- **Plotly** - Interactive charts
- **SciPy** - Statistical functions
- **ReportLab** - PDF generation
- **Kaleido** - Chart image export

## Project Structure

```
fabvariation/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── models/
│   ├── __init__.py
│   └── simulation_data.py          # Simulation data model
└── utils/
    ├── __init__.py
    ├── constants.py                # Configuration constants
    ├── calculations.py             # SPC calculations (limits, EWMA, CUSUM)
    ├── chart_utils.py              # Plotly chart generation
    ├── pdf_generator.py            # PDF report generation
    └── csv_exporter.py             # CSV export utilities
```

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

### Steps

1. **Clone or download this repository**

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

This will install all required packages:
- streamlit>=1.42.0
- pandas>=2.2.0
- numpy>=1.26.0
- plotly>=5.18.0
- scipy>=1.12.0
- reportlab>=4.0.0
- Pillow>=10.2.0
- kaleido>=0.2.1

## Running the Application

### Local Development

To run the application locally:

```bash
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8501`

### Command Line Options

```bash
# Run on a specific port
streamlit run app.py --server.port 8080

# Run without auto-opening browser
streamlit run app.py --server.headless true

# Run with custom theme
streamlit run app.py --theme.base dark
```

## Deployment to Streamlit Community Cloud

Deploy your app to the cloud in 2 clicks:

### Step 1: Prepare Your Repository

1. Push your code to GitHub (make sure `requirements.txt` is included)
2. Ensure all files are committed

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository, branch, and main file path (`app.py`)
5. Click "Deploy"

Your app will be live at: `https://[your-app-name].streamlit.app`

## Usage Guide

### Basic Workflow

1. **Select Process Type**: Choose from pre-configured semiconductor processes (Plasma Etch Rate, Wafer Thickness, etc.)

2. **Configure Parameters**:
   - Number of batches to simulate (10-100)
   - Sample size per batch (2-10)
   - Mean shift (process offset)
   - Sigma multiplier (variation level)

3. **Choose Drift Scenario**:
   - Stable Process: Normal variation only
   - Gradual Shift: Slow drift over time
   - Sudden Spike: Abrupt process excursion
   - Cyclic Drift: Periodic oscillation

4. **Select Chart Type**:
   - X-bar Chart: Monitor process average
   - Individuals Chart: Track individual measurements
   - EWMA Chart: Detect small persistent shifts
   - CUSUM Chart: Early drift detection

5. **Generate Simulation**: Click "Refresh Chart" to generate new data

6. **Inject Defects**: Test violation detection by clicking "Inject Defect"

7. **Export Results**:
   - Click "Save Log" to download CSV data
   - Click "Export PDF" for professional report

### Testing the Demo

**Scenario 1: Stable Process**
- Set drift scenario to "Stable Process"
- Click "Refresh Chart"
- Observe: Should show no violations (or very few)

**Scenario 2: Gradual Shift Detection**
- Set drift scenario to "Gradual Shift"
- Click "Refresh Chart"
- Observe: Western Electric Rule violations after midpoint

**Scenario 3: Sudden Spike**
- Set drift scenario to "Sudden Spike"
- Click "Refresh Chart"
- Observe: Critical violations (Rule 1) at 70% point

**Scenario 4: Manual Defect Injection**
- Generate any stable simulation
- Click "Inject Defect"
- Observe: Immediate violation alert and email notification

### Advanced Features

#### EWMA Configuration
- Lambda (λ): 0.05 - 0.30 (default 0.2)
  - Lower values = more smoothing
  - Higher values = more responsive

#### CUSUM Configuration
- Reference value (k): 0.1 - 1.0 (default 0.5)
- Decision interval (h): 3.0 - 8.0 (default 5.0)

## Understanding the Output

### Metrics Dashboard

- **Process Mean**: Current average vs. target
- **Process Std Dev**: Current variation vs. target
- **Violations Detected**: Number of rule violations
- **Estimated Scrap Cost**: Financial impact of out-of-control conditions

### Control Charts

Charts display:
- **Green line**: Process data (in control)
- **Pink X markers**: Violations detected
- **Green dashed line**: Center line (target)
- **Red dashed lines**: Upper/Lower Control Limits (3σ)
- **Orange dotted lines**: 2σ warning zones

### Violation Table

Lists all detected violations with:
- Batch number
- Rule violated (Western Electric or Nelson)
- Description
- Severity level (critical, major, moderate, minor)

## Technical Details

### Statistical Process Control (SPC) Rules

**Western Electric Rules**:
1. One point beyond 3σ limits
2. Two of three consecutive points beyond 2σ (same side)
3. Four of five consecutive points beyond 1σ (same side)
4. Eight consecutive points on one side of center line

**Nelson Rules**:
1. One point beyond 3σ
2. Nine consecutive points on same side
3. Six consecutive points trending
4. Fourteen consecutive points alternating
5. Two of three points beyond 2σ (same side)
6. Four of five points beyond 1σ (same side)

### Control Limit Calculations

**X-bar Chart**:
```
UCL = X̄ + A₂ × R̄
LCL = X̄ - A₂ × R̄
```

**EWMA Chart**:
```
EWMA₍ = λ × X₍ + (1-λ) × EWMA₍₋₁₎
UCL/LCL = μ ± L × σ × √(λ/(2-λ))
```

**CUSUM Chart**:
```
C⁺₍ = max(0, X₍ - μ - K + C⁺₍₋₁₎)
C⁻₍ = max(0, μ - X₍ - K + C⁻₍₋₁₎)
```

## Troubleshooting

### Common Issues

**Issue**: "ModuleNotFoundError"
- **Solution**: Run `pip install -r requirements.txt` again

**Issue**: Charts not displaying
- **Solution**: Ensure kaleido is installed: `pip install kaleido`

**Issue**: PDF export fails
- **Solution**: Check that reportlab is installed: `pip install reportlab`

**Issue**: Streamlit doesn't start
- **Solution**: Check Python version (must be 3.11+)

### Performance Tips

- For faster rendering, reduce number of batches to 20-30
- Large datasets (>100 batches) may take longer to export to PDF
- Use "Refresh Chart" button to regenerate data instead of page refresh

## Contributing

This is a production-ready tool designed for semiconductor manufacturing. Future enhancements could include:
- Real-time data integration with fab equipment
- Multi-process comparison views
- Historical trend analysis
- Custom rule configuration
- Integration with MES/LIMS systems

## License

This project is designed for educational and demonstration purposes for semiconductor manufacturing SPC applications.

## Support

For questions or issues:
1. Check the troubleshooting section above
2. Review the inline code comments (all files are heavily documented)
3. Consult Streamlit documentation: https://docs.streamlit.io

## Authors

Built by a data scientist who loves to pursue interests in industrial web dashboards for semiconductor and manufacturing companies.

---

**Ready to use?** Run `streamlit run app.py` and start monitoring your semiconductor processes!
