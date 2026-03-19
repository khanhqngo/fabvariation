# FabVariation Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- streamlit (web framework)
- pandas (data handling)
- numpy (calculations)
- plotly (charts)
- scipy (statistics)
- reportlab (PDF generation)
- Pillow (image processing)
- kaleido (chart export)

## Step 2: Verify Installation

Run the test script to check all dependencies:

```bash
python test_imports.py
```

You should see all checks pass with green checkmarks (✓).

## Step 3: Run the Application

### Option A: Simple Command

```bash
streamlit run app.py
```

### Option B: Use the Quick Start Script

```bash
./run.sh
```

The app will automatically open in your browser at: `http://localhost:8501`

## Step 4: Use the Application

### First Time Setup

1. The app loads automatically with **Plasma Etch Rate** process
2. Default simulation: 30 batches, stable process
3. You'll see:
   - Control chart (green line with data points)
   - Process metrics (mean, std dev, violations, cost)
   - No violations initially (stable process)

### Test Drive - 5 Minute Demo

**Demo 1: Stable Process (Already Running)**
- Current view shows stable process
- No violations should be detected
- Scrap cost = $0

**Demo 2: Inject a Defect**
1. Click "⚠️ Inject Defect" button
2. Watch the chart update with a violation marker (pink X)
3. See email alert appear at top
4. Scrap cost updates to $500

**Demo 3: Gradual Shift Detection**
1. In sidebar: Change "Drift Scenario" to "Gradual Shift"
2. Click "🔄 Refresh Chart"
3. Observe violations appearing after batch 15
4. Multiple Western Electric rules triggered

**Demo 4: Sudden Spike**
1. Change "Drift Scenario" to "Sudden Spike"
2. Click "🔄 Refresh Chart"
3. See critical violations (Rule 1) at 70% point
4. Email alert triggers automatically

**Demo 5: EWMA Chart (Small Shift Detection)**
1. Change "Chart Type" to "EWMA Chart"
2. Set "Drift Scenario" to "Gradual Shift"
3. Click "🔄 Refresh Chart"
4. Notice EWMA catches the shift earlier than X-bar

**Demo 6: Export Reports**
1. Click "📄 Export PDF" button
2. Download professional PDF report
3. Click "💾 Save Log" button
4. Download CSV data file

## Step 5: Explore Advanced Features

### Try Different Processes

In sidebar, select:
- **Wafer Thickness** (775 μm ± 2.5)
- **Deposition Rate** (1200 Å/min ± 15)
- **Resistivity** (10 Ω-cm ± 0.3)
- **Critical Dimension** (45 nm ± 0.8)

### Adjust Parameters

Experiment with:
- **Mean Shift**: -20 to +20 (simulates process offset)
- **Sigma Multiplier**: 0.5 to 3.0 (variation level)
- **Number of Batches**: 10 to 100
- **Sample Size**: 2 to 10 measurements per batch

### Chart Types

Compare different detection methods:
- **X-bar Chart**: Standard Shewhart chart for batch averages
- **Individuals Chart**: For single measurements
- **EWMA Chart**: Best for detecting small persistent shifts
- **CUSUM Chart**: Early warning system for gradual drift

### Advanced EWMA/CUSUM Settings

In sidebar, expand "Advanced Parameters":

**EWMA Settings:**
- Lambda (λ) = 0.2 (default)
  - Lower (0.05): More smoothing, slower response
  - Higher (0.25): Less smoothing, faster response

**CUSUM Settings:**
- k = 0.5 (reference value)
- h = 5.0 (decision interval)
  - Lower h: More sensitive, more false alarms
  - Higher h: Less sensitive, fewer false alarms

## Common Usage Patterns

### Pattern 1: Daily Process Monitoring Simulation
```
1. Select your process (e.g., Plasma Etch Rate)
2. Set to "Stable Process" drift
3. Run 30-50 batches
4. Check for any violations
5. Export PDF for daily report
```

### Pattern 2: Process Capability Study
```
1. Run multiple simulations with different sigma multipliers
2. Compare violation rates
3. Determine acceptable process variation limits
4. Export CSV for statistical analysis
```

### Pattern 3: SPC Training
```
1. Start with stable process
2. Show trainees how control charts work
3. Inject defects to demonstrate violation detection
4. Try different drift scenarios
5. Compare X-bar vs EWMA vs CUSUM effectiveness
```

## Troubleshooting

### App Won't Start

**Error**: "ModuleNotFoundError: No module named 'streamlit'"
- **Fix**: Run `pip install -r requirements.txt`

**Error**: "command not found: streamlit"
- **Fix**: Make sure Python and pip are in your PATH
- Try: `python -m streamlit run app.py`

### Charts Not Displaying

**Issue**: Blank chart area
- **Fix**: Install kaleido: `pip install kaleido`

### PDF Export Fails

**Issue**: Error when clicking "Export PDF"
- **Fix**: Install reportlab: `pip install reportlab`
- Also ensure Pillow is installed: `pip install Pillow`

### Performance Issues

**Issue**: App is slow with 100 batches
- **Fix**: Reduce to 30-50 batches for faster response
- Close other browser tabs
- Restart Streamlit if session becomes slow

## Tips & Best Practices

1. **Start Simple**: Begin with 30 batches, stable process
2. **One Change at a Time**: Adjust one parameter, then refresh
3. **Save Before Experimenting**: Save CSV log before trying extreme parameters
4. **Compare Charts**: Try the same data with different chart types
5. **Read Violations**: Click to expand violation table for details
6. **Export Regularly**: Generate PDFs to track patterns over time

## What's Next?

Now that you're familiar with FabVariation, you can:

1. **Simulate Real Scenarios**: Input your actual process parameters
2. **Train Team Members**: Use for SPC training sessions
3. **Evaluate Control Strategies**: Test different sample sizes and frequencies
4. **Deploy to Cloud**: Follow README for Streamlit Cloud deployment
5. **Customize**: Modify constants.py for your specific processes

## Getting Help

- **Documentation**: See full README.md
- **Code Comments**: All files heavily commented
- **Test Script**: Run `python test_imports.py` to verify setup
- **Streamlit Docs**: https://docs.streamlit.io

---

**Ready?** Run `streamlit run app.py` and start monitoring! 🚀
