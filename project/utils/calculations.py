"""
=== utils/calculations.py ===

This module contains all statistical process control (SPC) calculations including:
- Control limits for X-bar and R charts
- EWMA (Exponentially Weighted Moving Average) calculations
- CUSUM (Cumulative Sum) calculations
- Western Electric rules violation detection
- Nelson rules violation detection
- Process capability indices

All calculations follow standard SPC textbook formulas and industry best practices.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from utils.constants import (
    A2_FACTORS, D3_FACTORS, D4_FACTORS,
    EWMA_DEFAULTS, CUSUM_DEFAULTS
)


class SPCCalculator:
    """
    Statistical Process Control calculator for control charts and rule violations.
    """

    def __init__(self, target_mean: float, target_sigma: float):
        self.target_mean = target_mean
        self.target_sigma = target_sigma

    def calculate_xbar_limits(
        self,
        df: pd.DataFrame,
        sample_size: int
    ) -> Dict[str, float]:
        """
        Calculate control limits for X-bar chart.

        Args:
            df: DataFrame with 'x_bar' and 'range_r' columns
            sample_size: Number of measurements per subgroup

        Returns:
            Dictionary with UCL, LCL, center line, and sigma boundaries
        """
        if df.empty:
            return {}

        # Get A2 factor for sample size
        A2 = A2_FACTORS.get(sample_size, A2_FACTORS[5])

        # Calculate average of subgroup means (center line)
        x_double_bar = df['x_bar'].mean()

        # Calculate average range
        r_bar = df['range_r'].mean()

        # Control limits
        ucl = x_double_bar + A2 * r_bar
        lcl = x_double_bar - A2 * r_bar

        # Sigma boundaries (for Western Electric rules)
        sigma_xbar = r_bar / (np.sqrt(sample_size) * 1.128)  # d2 approximation

        return {
            'center_line': x_double_bar,
            'ucl': ucl,
            'lcl': lcl,
            'sigma_1_upper': x_double_bar + 1 * sigma_xbar,
            'sigma_1_lower': x_double_bar - 1 * sigma_xbar,
            'sigma_2_upper': x_double_bar + 2 * sigma_xbar,
            'sigma_2_lower': x_double_bar - 2 * sigma_xbar,
            'sigma_3_upper': ucl,
            'sigma_3_lower': lcl,
        }

    def calculate_individuals_limits(
        self,
        df: pd.DataFrame
    ) -> Dict[str, float]:
        """
        Calculate control limits for Individuals chart.

        Args:
            df: DataFrame with 'x_bar' column

        Returns:
            Dictionary with UCL, LCL, and center line
        """
        if df.empty:
            return {}

        # Calculate moving range
        moving_ranges = df['x_bar'].diff().abs()
        mr_bar = moving_ranges.mean()

        # Center line
        x_bar = df['x_bar'].mean()

        # Control limits for individuals chart
        # Using d2 constant for n=2 (moving range): 1.128
        ucl = x_bar + 2.66 * mr_bar
        lcl = x_bar - 2.66 * mr_bar

        sigma_est = mr_bar / 1.128

        return {
            'center_line': x_bar,
            'ucl': ucl,
            'lcl': lcl,
            'sigma_1_upper': x_bar + 1 * sigma_est,
            'sigma_1_lower': x_bar - 1 * sigma_est,
            'sigma_2_upper': x_bar + 2 * sigma_est,
            'sigma_2_lower': x_bar - 2 * sigma_est,
            'sigma_3_upper': ucl,
            'sigma_3_lower': lcl,
        }

    def calculate_ewma(
        self,
        df: pd.DataFrame,
        lambda_param: float = EWMA_DEFAULTS['lambda'],
        L: float = EWMA_DEFAULTS['L']
    ) -> Tuple[np.ndarray, Dict[str, float]]:
        """
        Calculate EWMA (Exponentially Weighted Moving Average) values and limits.

        Args:
            df: DataFrame with 'x_bar' column
            lambda_param: Smoothing parameter (0 < λ ≤ 1)
            L: Control limit multiplier (typically 2.7 - 3.0)

        Returns:
            Tuple of (EWMA values array, limits dictionary)
        """
        if df.empty:
            return np.array([]), {}

        values = df['x_bar'].values
        n_points = len(values)

        # Initialize EWMA array
        ewma = np.zeros(n_points)
        ewma[0] = values[0]  # First EWMA equals first observation

        # Calculate EWMA recursively
        for i in range(1, n_points):
            ewma[i] = lambda_param * values[i] + (1 - lambda_param) * ewma[i - 1]

        # Calculate control limits
        # Standard deviation of process (estimated from data)
        sigma = df['x_bar'].std()

        # EWMA control limits (vary with i)
        # For large i, limits approach steady-state
        # UCL/LCL = target ± L * sigma * sqrt(λ/(2-λ))

        steady_state_factor = np.sqrt(lambda_param / (2 - lambda_param))
        ucl = self.target_mean + L * sigma * steady_state_factor
        lcl = self.target_mean - L * sigma * steady_state_factor

        limits = {
            'center_line': self.target_mean,
            'ucl': ucl,
            'lcl': lcl,
        }

        return ewma, limits

    def calculate_cusum(
        self,
        df: pd.DataFrame,
        k: float = CUSUM_DEFAULTS['k'],
        h: float = CUSUM_DEFAULTS['h']
    ) -> Tuple[np.ndarray, np.ndarray, Dict[str, float]]:
        """
        Calculate CUSUM (Cumulative Sum) values and limits.

        Args:
            df: DataFrame with 'x_bar' column
            k: Reference value (typically 0.5 * sigma)
            h: Decision interval (typically 4-5 * sigma)

        Returns:
            Tuple of (C+ array, C- array, limits dictionary)
        """
        if df.empty:
            return np.array([]), np.array([]), {}

        values = df['x_bar'].values
        n_points = len(values)

        # K and H in actual units
        K = k * self.target_sigma
        H = h * self.target_sigma

        # Initialize CUSUM arrays
        c_plus = np.zeros(n_points)
        c_minus = np.zeros(n_points)

        # Calculate CUSUM recursively
        for i in range(n_points):
            if i == 0:
                c_plus[i] = max(0, values[i] - self.target_mean - K)
                c_minus[i] = max(0, self.target_mean - values[i] - K)
            else:
                c_plus[i] = max(0, values[i] - self.target_mean - K + c_plus[i - 1])
                c_minus[i] = max(0, self.target_mean - values[i] - K + c_minus[i - 1])

        limits = {
            'center_line': 0,
            'ucl': H,
            'lcl': -H,
        }

        return c_plus, c_minus, limits

    def detect_western_electric_violations(
        self,
        df: pd.DataFrame,
        limits: Dict[str, float]
    ) -> List[Dict]:
        """
        Detect Western Electric rules violations.

        Args:
            df: DataFrame with 'x_bar' column
            limits: Control limits dictionary

        Returns:
            List of violation dictionaries with batch, rule, and description
        """
        if df.empty or not limits:
            return []

        violations = []
        values = df['x_bar'].values
        batches = df['batch'].values

        center = limits['center_line']
        ucl = limits['ucl']
        lcl = limits['lcl']
        sigma_1_upper = limits.get('sigma_1_upper', center + self.target_sigma)
        sigma_1_lower = limits.get('sigma_1_lower', center - self.target_sigma)
        sigma_2_upper = limits.get('sigma_2_upper', center + 2 * self.target_sigma)
        sigma_2_lower = limits.get('sigma_2_lower', center - 2 * self.target_sigma)

        # Rule 1: One point beyond 3σ
        for i, val in enumerate(values):
            if val > ucl or val < lcl:
                violations.append({
                    'batch': int(batches[i]),
                    'rule': 'Western Electric Rule 1',
                    'description': f'Point beyond 3σ (value: {val:.2f})',
                    'severity': 'critical',
                })

        # Rule 2: Two of three beyond 2σ (same side)
        for i in range(2, len(values)):
            window = values[i-2:i+1]
            above_2sigma = sum(1 for v in window if v > sigma_2_upper)
            below_2sigma = sum(1 for v in window if v < sigma_2_lower)

            if above_2sigma >= 2:
                violations.append({
                    'batch': int(batches[i]),
                    'rule': 'Western Electric Rule 2',
                    'description': 'Two of three points beyond +2σ',
                    'severity': 'major',
                })
            if below_2sigma >= 2:
                violations.append({
                    'batch': int(batches[i]),
                    'rule': 'Western Electric Rule 2',
                    'description': 'Two of three points beyond -2σ',
                    'severity': 'major',
                })

        # Rule 3: Four of five beyond 1σ (same side)
        for i in range(4, len(values)):
            window = values[i-4:i+1]
            above_1sigma = sum(1 for v in window if v > sigma_1_upper)
            below_1sigma = sum(1 for v in window if v < sigma_1_lower)

            if above_1sigma >= 4:
                violations.append({
                    'batch': int(batches[i]),
                    'rule': 'Western Electric Rule 3',
                    'description': 'Four of five points beyond +1σ',
                    'severity': 'major',
                })
            if below_1sigma >= 4:
                violations.append({
                    'batch': int(batches[i]),
                    'rule': 'Western Electric Rule 3',
                    'description': 'Four of five points beyond -1σ',
                    'severity': 'major',
                })

        # Rule 4: Eight consecutive on one side
        for i in range(7, len(values)):
            window = values[i-7:i+1]
            if all(v > center for v in window):
                violations.append({
                    'batch': int(batches[i]),
                    'rule': 'Western Electric Rule 4',
                    'description': 'Eight consecutive points above center',
                    'severity': 'moderate',
                })
            elif all(v < center for v in window):
                violations.append({
                    'batch': int(batches[i]),
                    'rule': 'Western Electric Rule 4',
                    'description': 'Eight consecutive points below center',
                    'severity': 'moderate',
                })

        return violations

    def detect_nelson_violations(
        self,
        df: pd.DataFrame,
        limits: Dict[str, float]
    ) -> List[Dict]:
        """
        Detect Nelson rules violations.

        Args:
            df: DataFrame with 'x_bar' column
            limits: Control limits dictionary

        Returns:
            List of violation dictionaries
        """
        if df.empty or not limits:
            return []

        violations = []
        values = df['x_bar'].values
        batches = df['batch'].values

        center = limits['center_line']
        ucl = limits['ucl']
        lcl = limits['lcl']
        sigma_1_upper = limits.get('sigma_1_upper', center + self.target_sigma)
        sigma_1_lower = limits.get('sigma_1_lower', center - self.target_sigma)
        sigma_2_upper = limits.get('sigma_2_upper', center + 2 * self.target_sigma)
        sigma_2_lower = limits.get('sigma_2_lower', center - 2 * self.target_sigma)

        # Nelson 1: Point beyond 3σ (same as WE Rule 1)
        for i, val in enumerate(values):
            if val > ucl or val < lcl:
                violations.append({
                    'batch': int(batches[i]),
                    'rule': 'Nelson Rule 1',
                    'description': f'Point beyond 3σ (value: {val:.2f})',
                    'severity': 'critical',
                })

        # Nelson 2: Nine points in a row on same side
        for i in range(8, len(values)):
            window = values[i-8:i+1]
            if all(v > center for v in window):
                violations.append({
                    'batch': int(batches[i]),
                    'rule': 'Nelson Rule 2',
                    'description': 'Nine consecutive points above center',
                    'severity': 'moderate',
                })
            elif all(v < center for v in window):
                violations.append({
                    'batch': int(batches[i]),
                    'rule': 'Nelson Rule 2',
                    'description': 'Nine consecutive points below center',
                    'severity': 'moderate',
                })

        # Nelson 3: Six points in a row trending
        for i in range(5, len(values)):
            window = values[i-5:i+1]
            diffs = np.diff(window)
            if all(d > 0 for d in diffs):
                violations.append({
                    'batch': int(batches[i]),
                    'rule': 'Nelson Rule 3',
                    'description': 'Six points in a row increasing',
                    'severity': 'major',
                })
            elif all(d < 0 for d in diffs):
                violations.append({
                    'batch': int(batches[i]),
                    'rule': 'Nelson Rule 3',
                    'description': 'Six points in a row decreasing',
                    'severity': 'major',
                })

        # Nelson 4: Fourteen points alternating
        if len(values) >= 14:
            for i in range(13, len(values)):
                window = values[i-13:i+1]
                diffs = np.diff(window)
                alternating = all(diffs[j] * diffs[j+1] < 0 for j in range(len(diffs)-1))
                if alternating:
                    violations.append({
                        'batch': int(batches[i]),
                        'rule': 'Nelson Rule 4',
                        'description': 'Fourteen points alternating',
                        'severity': 'minor',
                    })

        return violations

    def calculate_process_capability(
        self,
        df: pd.DataFrame,
        usl: float,
        lsl: float
    ) -> Dict[str, float]:
        """
        Calculate process capability indices (Cp, Cpk).

        Args:
            df: DataFrame with 'x_bar' column
            usl: Upper specification limit
            lsl: Lower specification limit

        Returns:
            Dictionary with Cp, Cpk, and other capability metrics
        """
        if df.empty:
            return {}

        process_mean = df['x_bar'].mean()
        process_std = df['x_bar'].std()

        # Cp: Potential capability
        cp = (usl - lsl) / (6 * process_std)

        # Cpk: Actual capability (accounts for centering)
        cpu = (usl - process_mean) / (3 * process_std)
        cpl = (process_mean - lsl) / (3 * process_std)
        cpk = min(cpu, cpl)

        return {
            'cp': cp,
            'cpk': cpk,
            'cpu': cpu,
            'cpl': cpl,
            'process_mean': process_mean,
            'process_std': process_std,
        }


# ===== END OF FILE: utils/calculations.py =====
# This file handles all statistical calculations for SPC control charts.
# Used by: app.py and chart_utils.py for generating control charts with violation detection.
