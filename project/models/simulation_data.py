"""
=== models/simulation_data.py ===

This module defines the SimulationData class which manages all process measurement data,
including data generation, drift scenarios, and defect injection for semiconductor processes.

It provides methods to:
- Generate realistic process measurements with normal distribution
- Apply various drift patterns (stable, gradual shift, sudden spike, cyclic)
- Inject defects (outliers or shifts) into the measurement stream
- Track simulation history and metadata
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple


class SimulationData:
    """
    Manages simulation data for semiconductor process measurements.

    Attributes:
        process_name: Name of the process being simulated (e.g., "Plasma Etch Rate")
        process_unit: Unit of measurement (e.g., "nm", "Angstrom", "nm/min")
        target_mean: Target process mean value
        target_sigma: Target process standard deviation
        sample_size: Number of measurements per batch/subgroup
        drift_scenario: Type of drift pattern applied
    """

    def __init__(
        self,
        process_name: str = "Plasma Etch Rate",
        process_unit: str = "nm",
        target_mean: float = 500.0,
        target_sigma: float = 5.0,
        sample_size: int = 5
    ):
        self.process_name = process_name
        self.process_unit = process_unit
        self.target_mean = target_mean
        self.target_sigma = target_sigma
        self.sample_size = sample_size
        self.drift_scenario = "stable"

        # Initialize empty data storage
        self.measurements: List[float] = []
        self.batch_numbers: List[int] = []
        self.timestamps: List[datetime] = []
        self.defect_flags: List[bool] = []

        # History tracking
        self.simulation_id = self._generate_simulation_id()
        self.creation_time = datetime.now()

    def _generate_simulation_id(self) -> str:
        """Generate unique simulation ID."""
        return f"SIM_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def generate_data(
        self,
        num_batches: int = 30,
        mean_shift: float = 0.0,
        sigma_multiplier: float = 1.0,
        drift_scenario: str = "stable"
    ) -> pd.DataFrame:
        """
        Generate process measurement data with specified drift pattern.

        Args:
            num_batches: Number of batches to generate
            mean_shift: Shift to apply to the target mean
            sigma_multiplier: Multiplier for the standard deviation
            drift_scenario: Type of drift ("stable", "gradual_shift", "sudden_spike", "cyclic_drift")

        Returns:
            DataFrame with columns: batch, timestamp, measurement, x_bar, range_r, defect_injected
        """
        self.drift_scenario = drift_scenario

        # Clear existing data
        self.measurements = []
        self.batch_numbers = []
        self.timestamps = []
        self.defect_flags = []

        # Starting timestamp (simulate hourly batches)
        start_time = datetime.now() - timedelta(hours=num_batches)

        # Adjusted parameters
        adjusted_mean = self.target_mean + mean_shift
        adjusted_sigma = self.target_sigma * sigma_multiplier

        # Generate measurements batch by batch
        for batch_idx in range(num_batches):
            batch_time = start_time + timedelta(hours=batch_idx)

            # Apply drift pattern to mean
            drift_offset = self._calculate_drift_offset(batch_idx, num_batches)
            batch_mean = adjusted_mean + drift_offset

            # Generate individual measurements for this batch
            batch_measurements = np.random.normal(
                loc=batch_mean,
                scale=adjusted_sigma,
                size=self.sample_size
            )

            # Store each measurement
            for measurement in batch_measurements:
                self.measurements.append(measurement)
                self.batch_numbers.append(batch_idx + 1)
                self.timestamps.append(batch_time)
                self.defect_flags.append(False)

        return self.to_dataframe()

    def _calculate_drift_offset(self, batch_idx: int, total_batches: int) -> float:
        """
        Calculate drift offset based on scenario.

        Args:
            batch_idx: Current batch index
            total_batches: Total number of batches

        Returns:
            Offset value to add to the mean
        """
        if self.drift_scenario == "stable":
            return 0.0

        elif self.drift_scenario == "gradual_shift":
            # Gradual upward drift starting at 50% point
            if batch_idx > total_batches // 2:
                progress = (batch_idx - total_batches // 2) / (total_batches // 2)
                return progress * self.target_sigma * 3
            return 0.0

        elif self.drift_scenario == "sudden_spike":
            # Sudden spike at 70% point, lasting 3 batches
            spike_start = int(total_batches * 0.7)
            if spike_start <= batch_idx < spike_start + 3:
                return self.target_sigma * 4
            return 0.0

        elif self.drift_scenario == "cyclic_drift":
            # Sinusoidal drift
            cycle_length = total_batches / 3
            amplitude = self.target_sigma * 2
            return amplitude * np.sin(2 * np.pi * batch_idx / cycle_length)

        return 0.0

    def inject_defect(
        self,
        defect_type: str = "outlier",
        severity: float = 5.0
    ) -> None:
        """
        Inject a defect into the most recent measurements.

        Args:
            defect_type: Type of defect ("outlier" or "shift")
            severity: Severity multiplier (number of sigmas)
        """
        if len(self.measurements) < self.sample_size:
            return

        # Get the last batch of measurements
        last_batch_indices = list(range(len(self.measurements) - self.sample_size, len(self.measurements)))

        if defect_type == "outlier":
            # Inject one extreme outlier
            outlier_idx = last_batch_indices[-1]
            direction = np.random.choice([-1, 1])
            self.measurements[outlier_idx] += direction * severity * self.target_sigma
            self.defect_flags[outlier_idx] = True

        elif defect_type == "shift":
            # Shift all measurements in the last batch
            direction = np.random.choice([-1, 1])
            shift_amount = direction * severity * self.target_sigma
            for idx in last_batch_indices:
                self.measurements[idx] += shift_amount
                self.defect_flags[idx] = True

    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert current simulation data to a pandas DataFrame.

        Returns:
            DataFrame with batch statistics and individual measurements
        """
        if not self.measurements:
            return pd.DataFrame()

        # Create base dataframe
        df = pd.DataFrame({
            'batch': self.batch_numbers,
            'timestamp': self.timestamps,
            'measurement': self.measurements,
            'defect_injected': self.defect_flags
        })

        # Calculate batch statistics
        batch_stats = df.groupby('batch').agg({
            'measurement': ['mean', 'std', lambda x: x.max() - x.min(), 'count'],
            'timestamp': 'first',
            'defect_injected': 'any'
        }).reset_index()

        batch_stats.columns = ['batch', 'x_bar', 'std_dev', 'range_r', 'n', 'timestamp', 'defect_injected']

        return batch_stats

    def get_summary_stats(self) -> Dict[str, float]:
        """
        Calculate summary statistics for the simulation.

        Returns:
            Dictionary with overall mean, std dev, min, max, etc.
        """
        if not self.measurements:
            return {}

        measurements_array = np.array(self.measurements)

        return {
            'overall_mean': np.mean(measurements_array),
            'overall_std': np.std(measurements_array, ddof=1),
            'overall_min': np.min(measurements_array),
            'overall_max': np.max(measurements_array),
            'total_measurements': len(measurements_array),
            'num_batches': len(set(self.batch_numbers)),
            'num_defects_injected': sum(self.defect_flags)
        }

    def export_to_csv(self, filepath: str) -> None:
        """
        Export simulation data to CSV file.

        Args:
            filepath: Path to save the CSV file
        """
        df = self.to_dataframe()
        if not df.empty:
            df.to_csv(filepath, index=False)

    def load_from_csv(self, filepath: str) -> None:
        """
        Load simulation data from CSV file.

        Args:
            filepath: Path to the CSV file
        """
        df = pd.read_csv(filepath)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Reconstruct the simulation data (simplified)
        self.measurements = df['x_bar'].tolist() * self.sample_size
        self.batch_numbers = df['batch'].tolist() * self.sample_size
        self.timestamps = df['timestamp'].tolist() * self.sample_size
        self.defect_flags = df['defect_injected'].tolist() * self.sample_size


# ===== END OF FILE: models/simulation_data.py =====
# This file provides the core data model for the FabVariation simulator.
# It handles all data generation, drift patterns, and defect injection logic.
# Used by: app.py (main application) and csv_exporter.py (for data export)
