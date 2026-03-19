"""
=== utils/csv_exporter.py ===

This module handles CSV export functionality for simulation data.
Provides methods to:
- Export raw simulation data
- Export batch statistics
- Export violation logs
- Format data for Excel compatibility
"""

import pandas as pd
from typing import List, Dict
from datetime import datetime


class CSVExporter:
    """
    Handles CSV export operations for simulation data.
    """

    @staticmethod
    def export_simulation_data(
        df: pd.DataFrame,
        filepath: str,
        metadata: Dict = None
    ) -> None:
        """
        Export simulation data to CSV with optional metadata header.

        Args:
            df: DataFrame with simulation data
            filepath: Output file path
            metadata: Optional metadata to include as header comments
        """
        with open(filepath, 'w') as f:
            # Write metadata as comments
            if metadata:
                f.write(f"# FabVariation Simulation Export\n")
                f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Process: {metadata.get('process_name', 'N/A')}\n")
                f.write(f"# Drift Scenario: {metadata.get('drift_scenario', 'N/A')}\n")
                f.write(f"# Target Mean: {metadata.get('target_mean', 'N/A')}\n")
                f.write(f"# Target Sigma: {metadata.get('target_sigma', 'N/A')}\n")
                f.write(f"#\n")

            # Write dataframe
            df.to_csv(f, index=False)

    @staticmethod
    def export_violations(
        violations: List[Dict],
        filepath: str
    ) -> None:
        """
        Export violation log to CSV.

        Args:
            violations: List of violation dictionaries
            filepath: Output file path
        """
        if not violations:
            # Create empty dataframe with headers
            df = pd.DataFrame(columns=['batch', 'rule', 'description', 'severity'])
        else:
            df = pd.DataFrame(violations)

        df.to_csv(filepath, index=False)

    @staticmethod
    def export_summary_stats(
        summary_stats: Dict,
        filepath: str
    ) -> None:
        """
        Export summary statistics to CSV.

        Args:
            summary_stats: Summary statistics dictionary
            filepath: Output file path
        """
        # Convert dict to dataframe
        df = pd.DataFrame([summary_stats])

        # Transpose for better readability
        df_transposed = df.T
        df_transposed.columns = ['Value']
        df_transposed.index.name = 'Metric'

        df_transposed.to_csv(filepath)

    @staticmethod
    def create_combined_export(
        simulation_df: pd.DataFrame,
        violations: List[Dict],
        summary_stats: Dict,
        filepath: str,
        metadata: Dict = None
    ) -> None:
        """
        Create a single CSV file with multiple sheets' worth of data.
        (Note: CSV doesn't support multiple sheets, so we'll separate sections with blank lines)

        Args:
            simulation_df: Main simulation data
            violations: Violation log
            summary_stats: Summary statistics
            filepath: Output file path
            metadata: Optional metadata
        """
        with open(filepath, 'w') as f:
            # Header
            f.write("FabVariation Simulation - Combined Export\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

            if metadata:
                f.write(f"Process: {metadata.get('process_name', 'N/A')}\n")
                f.write(f"Drift Scenario: {metadata.get('drift_scenario', 'N/A')}\n")

            f.write("\n")

            # Section 1: Summary Statistics
            f.write("=== SUMMARY STATISTICS ===\n")
            summary_df = pd.DataFrame([summary_stats]).T
            summary_df.columns = ['Value']
            summary_df.to_csv(f)
            f.write("\n\n")

            # Section 2: Violations
            f.write("=== VIOLATIONS LOG ===\n")
            if violations:
                violations_df = pd.DataFrame(violations)
                violations_df.to_csv(f, index=False)
            else:
                f.write("No violations detected\n")
            f.write("\n\n")

            # Section 3: Batch Data
            f.write("=== BATCH STATISTICS ===\n")
            simulation_df.to_csv(f, index=False)

    @staticmethod
    def format_for_excel(
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Format dataframe for better Excel compatibility.

        Args:
            df: Input dataframe

        Returns:
            Formatted dataframe
        """
        df_formatted = df.copy()

        # Format timestamp columns
        if 'timestamp' in df_formatted.columns:
            df_formatted['timestamp'] = pd.to_datetime(df_formatted['timestamp'])
            df_formatted['timestamp'] = df_formatted['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # Round numeric columns to 2 decimal places
        numeric_columns = df_formatted.select_dtypes(include=['float64', 'float32']).columns
        for col in numeric_columns:
            df_formatted[col] = df_formatted[col].round(2)

        return df_formatted


# ===== END OF FILE: utils/csv_exporter.py =====
# This file handles CSV export functionality for all simulation data.
# Used by: app.py when user clicks "Download CSV" or "Save Simulation Log" buttons.
