"""
=== utils/constants.py ===

This module defines all constants, configuration values, and preset scenarios
used throughout the FabVariation application.

Includes:
- Color scheme definitions for charts and UI
- Preset process configurations
- Drift scenario definitions
- SPC control chart constants (A2, D3, D4 factors)
- Western Electric and Nelson rules definitions
"""

from typing import Dict, List, Tuple


# ========== COLOR SCHEME ==========
# Dark theme with green and orange accents for semiconductor fab aesthetic

COLORS = {
    'primary_green': '#00CC66',
    'primary_orange': '#FF6600',
    'background_dark': '#0E1117',
    'card_background': '#1E2127',
    'text_primary': '#FFFFFF',
    'text_secondary': '#B0B0B0',
    'border': '#2E3440',
    'ucl_color': '#FF4444',  # Upper Control Limit - Red
    'lcl_color': '#FF4444',  # Lower Control Limit - Red
    'warning_color': '#FFA500',  # Warning - Orange
    'target_color': '#00CC66',  # Target line - Green
    'violation_color': '#FF0066',  # Violation points - Bright pink
}


# ========== PROCESS PRESETS ==========
# Pre-configured semiconductor processes with realistic parameters

PROCESS_PRESETS = {
    'Plasma Etch Rate': {
        'unit': 'nm/min',
        'target_mean': 500.0,
        'target_sigma': 5.0,
        'description': 'Dry etch process for silicon dioxide removal',
        'wafer_cost': 500,
    },
    'Wafer Thickness': {
        'unit': 'um',
        'target_mean': 775.0,
        'target_sigma': 2.5,
        'description': 'Silicon wafer thickness after grinding',
        'wafer_cost': 450,
    },
    'Deposition Rate': {
        'unit': 'Angstrom/min',
        'target_mean': 1200.0,
        'target_sigma': 15.0,
        'description': 'Thin film deposition rate (CVD process)',
        'wafer_cost': 550,
    },
    'Resistivity': {
        'unit': 'Ohm-cm',
        'target_mean': 10.0,
        'target_sigma': 0.3,
        'description': 'Wafer resistivity measurement',
        'wafer_cost': 400,
    },
    'Critical Dimension': {
        'unit': 'nm',
        'target_mean': 45.0,
        'target_sigma': 0.8,
        'description': 'Lithography feature size (CD)',
        'wafer_cost': 600,
    },
}


# ========== DRIFT SCENARIOS ==========
# Predefined drift patterns for simulation

DRIFT_SCENARIOS = {
    'stable': {
        'name': 'Stable Process',
        'description': 'Normal variation only, no drift or shift',
        'icon': '✓',
    },
    'gradual_shift': {
        'name': 'Gradual Shift',
        'description': 'Process mean drifts upward gradually over time',
        'icon': '↗',
    },
    'sudden_spike': {
        'name': 'Sudden Spike',
        'description': 'Abrupt shift in process mean for several batches',
        'icon': '⚡',
    },
    'cyclic_drift': {
        'name': 'Cyclic Drift',
        'description': 'Sinusoidal oscillation in process mean',
        'icon': '〰',
    },
}


# ========== SPC CONTROL CHART CONSTANTS ==========
# A2, D3, D4 factors for X-bar and R charts (sample size 2-10)

# A2 factors for X-bar chart (3-sigma limits based on average range)
A2_FACTORS = {
    2: 1.880,
    3: 1.023,
    4: 0.729,
    5: 0.577,
    6: 0.483,
    7: 0.419,
    8: 0.373,
    9: 0.337,
    10: 0.308,
}

# D3 factors for R chart lower control limit
D3_FACTORS = {
    2: 0.0,
    3: 0.0,
    4: 0.0,
    5: 0.0,
    6: 0.0,
    7: 0.076,
    8: 0.136,
    9: 0.184,
    10: 0.223,
}

# D4 factors for R chart upper control limit
D4_FACTORS = {
    2: 3.267,
    3: 2.574,
    4: 2.282,
    5: 2.114,
    6: 2.004,
    7: 1.924,
    8: 1.864,
    9: 1.816,
    10: 1.777,
}


# ========== WESTERN ELECTRIC RULES ==========
# Standard Western Electric rules for control chart violations

WESTERN_ELECTRIC_RULES = {
    'rule_1': {
        'name': 'One point beyond 3σ',
        'description': 'Any single point falls outside the 3-sigma control limits',
        'severity': 'critical',
    },
    'rule_2': {
        'name': 'Two of three beyond 2σ',
        'description': 'Two out of three consecutive points fall beyond 2-sigma limits (same side)',
        'severity': 'major',
    },
    'rule_3': {
        'name': 'Four of five beyond 1σ',
        'description': 'Four out of five consecutive points fall beyond 1-sigma limits (same side)',
        'severity': 'major',
    },
    'rule_4': {
        'name': 'Eight consecutive on one side',
        'description': 'Eight consecutive points fall on one side of the center line',
        'severity': 'moderate',
    },
}


# ========== NELSON RULES ==========
# Nelson rules for detecting special cause variation

NELSON_RULES = {
    'nelson_1': {
        'name': 'Point beyond 3σ',
        'description': 'One point is more than 3 standard deviations from the mean',
        'severity': 'critical',
    },
    'nelson_2': {
        'name': 'Nine points in a row on same side',
        'description': 'Nine (or more) points in a row are on the same side of the mean',
        'severity': 'moderate',
    },
    'nelson_3': {
        'name': 'Six points in a row trending',
        'description': 'Six (or more) points in a row are continually increasing or decreasing',
        'severity': 'major',
    },
    'nelson_4': {
        'name': 'Fourteen points alternating',
        'description': 'Fourteen (or more) points in a row alternate in direction',
        'severity': 'minor',
    },
    'nelson_5': {
        'name': 'Two of three beyond 2σ',
        'description': 'Two out of three points in a row are more than 2σ from mean (same side)',
        'severity': 'major',
    },
    'nelson_6': {
        'name': 'Four of five beyond 1σ',
        'description': 'Four out of five points in a row are more than 1σ from mean (same side)',
        'severity': 'major',
    },
}


# ========== EWMA PARAMETERS ==========
# Exponentially Weighted Moving Average control chart parameters

EWMA_DEFAULTS = {
    'lambda': 0.2,  # Smoothing parameter (typical range: 0.05 - 0.25)
    'L': 3.0,  # Control limit multiplier (typically 2.7 - 3.0)
}


# ========== CUSUM PARAMETERS ==========
# Cumulative Sum control chart parameters

CUSUM_DEFAULTS = {
    'k': 0.5,  # Reference value (typically 0.5 * sigma)
    'h': 5.0,  # Decision interval (typically 4 - 5 * sigma)
}


# ========== CHART TYPE CONFIGURATIONS ==========

CHART_TYPES = {
    'xbar': {
        'name': 'X-bar Chart',
        'description': 'Average of subgroup measurements',
        'best_for': 'Detecting shifts in process mean',
    },
    'individuals': {
        'name': 'Individuals Chart',
        'description': 'Individual measurement values',
        'best_for': 'Single measurements per batch',
    },
    'ewma': {
        'name': 'EWMA Chart',
        'description': 'Exponentially weighted moving average',
        'best_for': 'Detecting small persistent shifts',
    },
    'cusum': {
        'name': 'CUSUM Chart',
        'description': 'Cumulative sum of deviations',
        'best_for': 'Early detection of process drift',
    },
}


# ========== DEFECT INJECTION OPTIONS ==========

DEFECT_TYPES = {
    'outlier': {
        'name': 'Single Outlier',
        'description': 'Inject one extreme measurement in the last batch',
    },
    'shift': {
        'name': 'Mean Shift',
        'description': 'Shift all measurements in the last batch',
    },
}


# ========== UI CONFIGURATION ==========

UI_CONFIG = {
    'page_title': 'FabVariation - Process Variation Simulator',
    'page_icon': '🔬',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
}


# ========== ALERT THRESHOLDS ==========

ALERT_THRESHOLDS = {
    'critical': {
        'color': COLORS['violation_color'],
        'priority': 1,
    },
    'major': {
        'color': COLORS['primary_orange'],
        'priority': 2,
    },
    'moderate': {
        'color': COLORS['warning_color'],
        'priority': 3,
    },
    'minor': {
        'color': COLORS['primary_green'],
        'priority': 4,
    },
}


# ===== END OF FILE: utils/constants.py =====
# This file centralizes all configuration constants for the application.
# Used by: All other modules for consistent styling, parameters, and configuration.
