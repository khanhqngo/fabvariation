# FabVariation File Structure

Complete reference for all files in the project.

## Root Directory

```
fabvariation/
├── app.py                      # Main Streamlit application (ENTRY POINT)
├── requirements.txt            # Python dependencies
├── README.md                   # Comprehensive documentation
├── QUICKSTART.md              # 5-minute getting started guide
├── FILE_STRUCTURE.md          # This file - project structure reference
├── test_imports.py            # Dependency verification script
├── run.sh                     # Quick start shell script (Linux/Mac)
├── .gitignore                 # Git ignore rules for Python/Streamlit
├── .streamlit/                # Streamlit configuration
│   └── config.toml            # Dark theme configuration
├── models/                    # Data models
│   ├── __init__.py           # Package initialization
│   └── simulation_data.py    # SimulationData class - core data model
└── utils/                     # Utility modules
    ├── __init__.py           # Package initialization
    ├── constants.py          # Configuration constants and presets
    ├── calculations.py       # SPC calculations (limits, EWMA, CUSUM, rules)
    ├── chart_utils.py        # Plotly chart generation
    ├── pdf_generator.py      # PDF report generation with ReportLab
    └── csv_exporter.py       # CSV export utilities
```

## File Descriptions

### Core Application Files

#### `app.py` (1,000+ lines)
**Purpose**: Main Streamlit web application

**Key Functions**:
- `main()` - Application entry point
- `apply_custom_css()` - Dark theme styling
- `initialize_session_state()` - Session management
- `generate_simulation()` - Create simulation data
- `calculate_violations()` - Detect rule violations
- `inject_defect_action()` - Add defects to data
- `display_simulation_results()` - Render charts and metrics
- `display_email_alert()` - Show alert notifications
- `save_simulation_log()` - Export CSV
- `export_pdf_report()` - Generate PDF reports

**Dependencies**: All modules (models, utils)

**Entry Point**: Run with `streamlit run app.py`

---

#### `requirements.txt` (8 lines)
**Purpose**: Python package dependencies

**Packages**:
- streamlit>=1.42.0 (web framework)
- pandas>=2.2.0 (data manipulation)
- numpy>=1.26.0 (numerical computing)
- plotly>=5.18.0 (interactive charts)
- scipy>=1.12.0 (statistical functions)
- reportlab>=4.0.0 (PDF generation)
- Pillow>=10.2.0 (image processing)
- kaleido>=0.2.1 (chart image export)

**Usage**: `pip install -r requirements.txt`

---

### Models Package

#### `models/__init__.py`
**Purpose**: Package initialization, exports SimulationData

#### `models/simulation_data.py` (300+ lines)
**Purpose**: Core data model for process measurements

**Class**: `SimulationData`

**Key Methods**:
- `generate_data()` - Generate measurement data with drift patterns
- `_calculate_drift_offset()` - Apply drift scenarios
- `inject_defect()` - Add outliers or shifts
- `to_dataframe()` - Convert to pandas DataFrame
- `get_summary_stats()` - Calculate statistics
- `export_to_csv()` - Save to file
- `load_from_csv()` - Load from file

**Attributes**:
- process_name, process_unit
- target_mean, target_sigma
- sample_size, drift_scenario
- measurements, batch_numbers, timestamps

**Used By**: app.py

---

### Utils Package

#### `utils/__init__.py`
**Purpose**: Package initialization, exports utility classes

#### `utils/constants.py` (250+ lines)
**Purpose**: All configuration constants and presets

**Key Constants**:
- `COLORS` - Dark theme color scheme
- `PROCESS_PRESETS` - 5 semiconductor processes with parameters
- `DRIFT_SCENARIOS` - 4 drift pattern definitions
- `A2_FACTORS`, `D3_FACTORS`, `D4_FACTORS` - SPC chart factors
- `WESTERN_ELECTRIC_RULES` - 4 rule definitions
- `NELSON_RULES` - 6 rule definitions
- `EWMA_DEFAULTS` - Lambda and L values
- `CUSUM_DEFAULTS` - k and h values
- `CHART_TYPES` - 4 chart type configurations
- `UI_CONFIG` - Page configuration

**Used By**: All modules

---

#### `utils/calculations.py` (450+ lines)
**Purpose**: Statistical Process Control calculations

**Class**: `SPCCalculator`

**Key Methods**:
- `calculate_xbar_limits()` - X-bar chart control limits
- `calculate_individuals_limits()` - Individuals chart limits
- `calculate_ewma()` - EWMA values and limits
- `calculate_cusum()` - CUSUM C+ and C- values
- `detect_western_electric_violations()` - Apply WE rules
- `detect_nelson_violations()` - Apply Nelson rules
- `calculate_process_capability()` - Cp, Cpk indices

**Formulas**:
- X-bar: UCL/LCL = X̄ ± A₂R̄
- EWMA: EWMA_i = λX_i + (1-λ)EWMA_{i-1}
- CUSUM: C⁺_i = max(0, X_i - μ - K + C⁺_{i-1})

**Used By**: app.py, chart_utils.py

---

#### `utils/chart_utils.py` (400+ lines)
**Purpose**: Interactive Plotly chart generation

**Class**: `ChartBuilder`

**Key Methods**:
- `_create_dark_template()` - Dark theme settings
- `create_xbar_chart()` - X-bar control chart
- `create_individuals_chart()` - Individuals chart
- `create_ewma_chart()` - EWMA chart
- `create_cusum_chart()` - CUSUM chart
- `create_range_chart()` - Range chart

**Chart Features**:
- Dark theme styling
- Control limits (UCL, LCL, center line)
- Sigma zones (1σ, 2σ, 3σ)
- Violation highlighting (pink X markers)
- Interactive hover tooltips
- Professional annotations

**Used By**: app.py

---

#### `utils/pdf_generator.py` (350+ lines)
**Purpose**: Professional PDF report generation

**Class**: `PDFReportGenerator`

**Key Methods**:
- `generate_report()` - Create complete PDF report
- `_create_header()` - Title and branding
- `_create_metadata_section()` - Simulation details
- `_create_summary_section()` - Statistics table
- `_create_cost_section()` - Scrap cost analysis
- `_create_violations_section()` - Violation log table
- `_create_charts_section()` - Embedded chart images
- `_create_footer()` - Report footer

**Report Sections**:
1. Header with title and timestamp
2. Simulation metadata
3. Summary statistics table
4. Scrap cost analysis
5. Violations log (color-coded by severity)
6. Control chart images
7. Footer with app info

**Used By**: app.py

---

#### `utils/csv_exporter.py` (175+ lines)
**Purpose**: CSV export functionality

**Class**: `CSVExporter`

**Key Methods**:
- `export_simulation_data()` - Export with metadata header
- `export_violations()` - Export violation log
- `export_summary_stats()` - Export statistics
- `create_combined_export()` - Multi-section CSV
- `format_for_excel()` - Excel-friendly formatting

**Export Formats**:
- CSV with comment headers (# prefix)
- Properly formatted timestamps
- Rounded numeric values
- Excel-compatible

**Used By**: app.py

---

### Configuration Files

#### `.streamlit/config.toml`
**Purpose**: Streamlit app configuration

**Settings**:
- Dark theme colors
- Primary/secondary colors
- Font settings
- Server configuration
- Browser settings

---

#### `.gitignore`
**Purpose**: Git ignore rules for Python/Streamlit projects

**Ignores**:
- Python cache (__pycache__, *.pyc)
- Virtual environments (venv/, env/)
- IDE files (.vscode/, .idea/)
- OS files (.DS_Store, Thumbs.db)
- Streamlit secrets
- Log files
- Temporary files

---

### Utility Scripts

#### `test_imports.py`
**Purpose**: Verify all dependencies are installed

**Usage**:
```bash
python test_imports.py
```

**Output**: Checkmarks (✓) for installed packages, X for missing

---

#### `run.sh`
**Purpose**: Quick start shell script

**Features**:
- Checks Python installation
- Auto-installs dependencies if needed
- Launches Streamlit app

**Usage**:
```bash
chmod +x run.sh
./run.sh
```

---

### Documentation Files

#### `README.md` (500+ lines)
**Purpose**: Comprehensive project documentation

**Sections**:
- Features overview
- Technology stack
- Installation instructions
- Usage guide with examples
- Deployment to Streamlit Cloud
- Technical details (SPC formulas)
- Troubleshooting
- API reference

---

#### `QUICKSTART.md` (400+ lines)
**Purpose**: 5-minute getting started guide

**Sections**:
- 5-step setup process
- Test drive scenarios (6 demos)
- Advanced features guide
- Common usage patterns
- Troubleshooting tips
- Best practices

---

#### `FILE_STRUCTURE.md` (This file)
**Purpose**: Complete file structure reference

---

## Import Dependencies Map

```
app.py
├── models.simulation_data
│   └── SimulationData
├── utils.constants
│   └── COLORS, PROCESS_PRESETS, DRIFT_SCENARIOS, etc.
├── utils.calculations
│   └── SPCCalculator
├── utils.chart_utils
│   └── ChartBuilder
├── utils.pdf_generator
│   └── PDFReportGenerator
└── utils.csv_exporter
    └── CSVExporter

models/simulation_data.py
├── numpy
├── pandas
└── datetime

utils/calculations.py
├── numpy
├── pandas
├── scipy (optional, not used currently)
└── utils.constants

utils/chart_utils.py
├── plotly.graph_objects
├── pandas
├── numpy
├── utils.constants
└── utils.calculations

utils/pdf_generator.py
├── reportlab (multiple modules)
├── io
├── datetime
└── plotly.graph_objects

utils/csv_exporter.py
├── pandas
└── datetime
```

## Execution Flow

1. **User runs**: `streamlit run app.py`

2. **App initialization**:
   - Load configuration from `.streamlit/config.toml`
   - Apply custom CSS styling
   - Initialize session state

3. **First load**:
   - Create `SimulationData` object
   - Generate initial data with default parameters
   - Calculate control limits with `SPCCalculator`
   - Detect violations
   - Generate charts with `ChartBuilder`

4. **User interactions**:
   - Parameter changes → trigger `generate_simulation()`
   - "Refresh Chart" → regenerate data
   - "Inject Defect" → call `inject_defect_action()`
   - "Export PDF" → `export_pdf_report()`
   - "Save Log" → `save_simulation_log()`

5. **Real-time updates**:
   - Streamlit re-runs affected sections
   - Session state persists data between interactions
   - Charts update with new violation highlights

## Code Organization Principles

1. **Separation of Concerns**:
   - Models: Data structure and generation
   - Utils: Reusable calculations and utilities
   - App: UI and user interaction logic

2. **Single Responsibility**:
   - Each class has one clear purpose
   - Each function does one thing well

3. **Dependency Injection**:
   - Calculator receives target parameters
   - Chart builder receives processed data
   - PDF generator receives all required data

4. **Configuration over Code**:
   - All constants in `constants.py`
   - Easy to modify presets without touching logic
   - Color scheme centralized

5. **Type Hints**:
   - All functions have type annotations
   - Clear parameter and return types
   - Better IDE support and error catching

## File Size Reference

- **Largest files** (most complex):
  1. app.py (~1000 lines) - Main application
  2. calculations.py (~450 lines) - SPC algorithms
  3. chart_utils.py (~400 lines) - Chart generation
  4. pdf_generator.py (~350 lines) - PDF reports
  5. simulation_data.py (~300 lines) - Data model

- **Configuration files**:
  - constants.py (~250 lines) - All presets
  - csv_exporter.py (~175 lines) - Export utilities

- **Documentation**:
  - README.md (~500 lines)
  - QUICKSTART.md (~400 lines)
  - FILE_STRUCTURE.md (~350 lines)

**Total Project**: ~4000 lines of Python code + 1250 lines of documentation

---

**For Developers**: Start by reading `README.md`, then explore `constants.py` to understand configuration, followed by `simulation_data.py` for the data model.

**For Users**: Read `QUICKSTART.md` and run `python test_imports.py` to get started in 5 minutes.
