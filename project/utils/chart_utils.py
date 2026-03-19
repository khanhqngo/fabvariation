"""
=== utils/chart_utils.py ===

This module handles all chart generation using Plotly.
Creates interactive control charts with:
- X-bar charts
- Individuals charts
- EWMA charts
- CUSUM charts
- Control limits and sigma zones
- Violation highlighting
- Professional dark theme styling
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from utils.constants import COLORS
from utils.calculations import SPCCalculator


class ChartBuilder:
    """
    Builds interactive Plotly charts for SPC visualization.
    """

    def __init__(self):
        self.colors = COLORS
        self.dark_template = self._create_dark_template()

    def _create_dark_template(self) -> Dict:
        """
        Create custom dark theme template for Plotly charts.

        Returns:
            Dictionary with Plotly layout settings
        """
        return {
            'paper_bgcolor': self.colors['background_dark'],
            'plot_bgcolor': self.colors['card_background'],
            'font': {
                'color': self.colors['text_primary'],
                'family': 'Inter, sans-serif',
                'size': 12,
            },
            'xaxis': {
                'gridcolor': self.colors['border'],
                'linecolor': self.colors['border'],
                'zerolinecolor': self.colors['border'],
            },
            'yaxis': {
                'gridcolor': self.colors['border'],
                'linecolor': self.colors['border'],
                'zerolinecolor': self.colors['border'],
            },
        }

    def create_xbar_chart(
        self,
        df: pd.DataFrame,
        limits: Dict[str, float],
        violations: List[Dict],
        process_name: str,
        process_unit: str
    ) -> go.Figure:
        """
        Create X-bar control chart with control limits and violation highlighting.

        Args:
            df: DataFrame with batch statistics
            limits: Control limits dictionary
            violations: List of violation dictionaries
            process_name: Name of the process
            process_unit: Unit of measurement

        Returns:
            Plotly Figure object
        """
        fig = go.Figure()

        # Get violation batches for highlighting
        violation_batches = [v['batch'] for v in violations]

        # Separate normal and violation points
        normal_mask = ~df['batch'].isin(violation_batches)
        violation_mask = df['batch'].isin(violation_batches)

        # Add main data points (normal)
        fig.add_trace(go.Scatter(
            x=df[normal_mask]['batch'],
            y=df[normal_mask]['x_bar'],
            mode='lines+markers',
            name='X-bar (Normal)',
            line=dict(color=self.colors['primary_green'], width=2),
            marker=dict(size=8, color=self.colors['primary_green']),
        ))

        # Add violation points (highlighted)
        if violation_mask.any():
            fig.add_trace(go.Scatter(
                x=df[violation_mask]['batch'],
                y=df[violation_mask]['x_bar'],
                mode='markers',
                name='Violations',
                marker=dict(
                    size=12,
                    color=self.colors['violation_color'],
                    symbol='x',
                    line=dict(width=2, color=self.colors['violation_color'])
                ),
            ))

        # Add control limits
        fig.add_hline(
            y=limits['center_line'],
            line_dash='solid',
            line_color=self.colors['target_color'],
            line_width=2,
            annotation_text='Center Line',
            annotation_position='right',
        )

        fig.add_hline(
            y=limits['ucl'],
            line_dash='dash',
            line_color=self.colors['ucl_color'],
            line_width=2,
            annotation_text='UCL (3σ)',
            annotation_position='right',
        )

        fig.add_hline(
            y=limits['lcl'],
            line_dash='dash',
            line_color=self.colors['lcl_color'],
            line_width=2,
            annotation_text='LCL (3σ)',
            annotation_position='right',
        )

        # Add sigma zones (2σ)
        fig.add_hline(
            y=limits.get('sigma_2_upper'),
            line_dash='dot',
            line_color=self.colors['warning_color'],
            line_width=1,
            opacity=0.5,
            annotation_text='2σ',
            annotation_position='right',
        )

        fig.add_hline(
            y=limits.get('sigma_2_lower'),
            line_dash='dot',
            line_color=self.colors['warning_color'],
            line_width=1,
            opacity=0.5,
            annotation_text='-2σ',
            annotation_position='right',
        )

        # Update layout
        fig.update_layout(
            title=f'{process_name} - X-bar Control Chart',
            xaxis_title='Batch Number',
            yaxis_title=f'Average {process_name} ({process_unit})',
            **self.dark_template,
            hovermode='x unified',
            height=500,
            showlegend=True,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            ),
        )

        return fig

    def create_individuals_chart(
        self,
        df: pd.DataFrame,
        limits: Dict[str, float],
        violations: List[Dict],
        process_name: str,
        process_unit: str
    ) -> go.Figure:
        """
        Create Individuals control chart.

        Args:
            df: DataFrame with batch statistics
            limits: Control limits dictionary
            violations: List of violation dictionaries
            process_name: Name of the process
            process_unit: Unit of measurement

        Returns:
            Plotly Figure object
        """
        fig = go.Figure()

        violation_batches = [v['batch'] for v in violations]
        normal_mask = ~df['batch'].isin(violation_batches)
        violation_mask = df['batch'].isin(violation_batches)

        # Add normal points
        fig.add_trace(go.Scatter(
            x=df[normal_mask]['batch'],
            y=df[normal_mask]['x_bar'],
            mode='lines+markers',
            name='Individual Values',
            line=dict(color=self.colors['primary_green'], width=2),
            marker=dict(size=8, color=self.colors['primary_green']),
        ))

        # Add violation points
        if violation_mask.any():
            fig.add_trace(go.Scatter(
                x=df[violation_mask]['batch'],
                y=df[violation_mask]['x_bar'],
                mode='markers',
                name='Violations',
                marker=dict(
                    size=12,
                    color=self.colors['violation_color'],
                    symbol='x',
                    line=dict(width=2)
                ),
            ))

        # Add control limits
        fig.add_hline(y=limits['center_line'], line_dash='solid',
                      line_color=self.colors['target_color'], line_width=2,
                      annotation_text='Center', annotation_position='right')
        fig.add_hline(y=limits['ucl'], line_dash='dash',
                      line_color=self.colors['ucl_color'], line_width=2,
                      annotation_text='UCL', annotation_position='right')
        fig.add_hline(y=limits['lcl'], line_dash='dash',
                      line_color=self.colors['lcl_color'], line_width=2,
                      annotation_text='LCL', annotation_position='right')

        fig.update_layout(
            title=f'{process_name} - Individuals Control Chart',
            xaxis_title='Batch Number',
            yaxis_title=f'{process_name} ({process_unit})',
            **self.dark_template,
            hovermode='x unified',
            height=500,
            showlegend=True,
        )

        return fig

    def create_ewma_chart(
        self,
        df: pd.DataFrame,
        ewma_values: np.ndarray,
        limits: Dict[str, float],
        process_name: str,
        process_unit: str,
        lambda_param: float
    ) -> go.Figure:
        """
        Create EWMA (Exponentially Weighted Moving Average) control chart.

        Args:
            df: DataFrame with batch statistics
            ewma_values: Calculated EWMA values
            limits: Control limits dictionary
            process_name: Name of the process
            process_unit: Unit of measurement
            lambda_param: EWMA smoothing parameter

        Returns:
            Plotly Figure object
        """
        fig = go.Figure()

        # Add EWMA line
        fig.add_trace(go.Scatter(
            x=df['batch'],
            y=ewma_values,
            mode='lines+markers',
            name=f'EWMA (λ={lambda_param})',
            line=dict(color=self.colors['primary_green'], width=3),
            marker=dict(size=6, color=self.colors['primary_green']),
        ))

        # Add original data (faded)
        fig.add_trace(go.Scatter(
            x=df['batch'],
            y=df['x_bar'],
            mode='lines',
            name='Original Data',
            line=dict(color=self.colors['text_secondary'], width=1, dash='dot'),
            opacity=0.4,
        ))

        # Add control limits
        fig.add_hline(y=limits['center_line'], line_dash='solid',
                      line_color=self.colors['target_color'], line_width=2,
                      annotation_text='Target', annotation_position='right')
        fig.add_hline(y=limits['ucl'], line_dash='dash',
                      line_color=self.colors['ucl_color'], line_width=2,
                      annotation_text='UCL', annotation_position='right')
        fig.add_hline(y=limits['lcl'], line_dash='dash',
                      line_color=self.colors['lcl_color'], line_width=2,
                      annotation_text='LCL', annotation_position='right')

        fig.update_layout(
            title=f'{process_name} - EWMA Chart',
            xaxis_title='Batch Number',
            yaxis_title=f'EWMA {process_name} ({process_unit})',
            **self.dark_template,
            hovermode='x unified',
            height=500,
            showlegend=True,
        )

        return fig

    def create_cusum_chart(
        self,
        df: pd.DataFrame,
        c_plus: np.ndarray,
        c_minus: np.ndarray,
        limits: Dict[str, float],
        process_name: str,
        process_unit: str
    ) -> go.Figure:
        """
        Create CUSUM (Cumulative Sum) control chart.

        Args:
            df: DataFrame with batch statistics
            c_plus: Positive CUSUM values
            c_minus: Negative CUSUM values
            limits: Control limits dictionary
            process_name: Name of the process
            process_unit: Unit of measurement

        Returns:
            Plotly Figure object
        """
        fig = go.Figure()

        # Add C+ (upward CUSUM)
        fig.add_trace(go.Scatter(
            x=df['batch'],
            y=c_plus,
            mode='lines+markers',
            name='C+ (Upward)',
            line=dict(color=self.colors['primary_orange'], width=2),
            marker=dict(size=6, color=self.colors['primary_orange']),
        ))

        # Add C- (downward CUSUM)
        fig.add_trace(go.Scatter(
            x=df['batch'],
            y=-c_minus,  # Negative for plotting below zero
            mode='lines+markers',
            name='C- (Downward)',
            line=dict(color=self.colors['primary_green'], width=2),
            marker=dict(size=6, color=self.colors['primary_green']),
        ))

        # Add control limits
        fig.add_hline(y=0, line_dash='solid',
                      line_color=self.colors['text_secondary'], line_width=1)
        fig.add_hline(y=limits['ucl'], line_dash='dash',
                      line_color=self.colors['ucl_color'], line_width=2,
                      annotation_text='H (Decision)', annotation_position='right')
        fig.add_hline(y=-limits['ucl'], line_dash='dash',
                      line_color=self.colors['lcl_color'], line_width=2,
                      annotation_text='-H (Decision)', annotation_position='right')

        fig.update_layout(
            title=f'{process_name} - CUSUM Chart',
            xaxis_title='Batch Number',
            yaxis_title=f'Cumulative Sum ({process_unit})',
            **self.dark_template,
            hovermode='x unified',
            height=500,
            showlegend=True,
        )

        return fig

    def create_range_chart(
        self,
        df: pd.DataFrame,
        sample_size: int,
        process_name: str,
        process_unit: str
    ) -> go.Figure:
        """
        Create Range (R) control chart.

        Args:
            df: DataFrame with 'range_r' column
            sample_size: Sample size for D3/D4 factors
            process_name: Name of the process
            process_unit: Unit of measurement

        Returns:
            Plotly Figure object
        """
        from utils.constants import D3_FACTORS, D4_FACTORS

        fig = go.Figure()

        r_bar = df['range_r'].mean()
        D3 = D3_FACTORS.get(sample_size, 0)
        D4 = D4_FACTORS.get(sample_size, 2.114)

        ucl_r = D4 * r_bar
        lcl_r = D3 * r_bar

        fig.add_trace(go.Scatter(
            x=df['batch'],
            y=df['range_r'],
            mode='lines+markers',
            name='Range',
            line=dict(color=self.colors['primary_orange'], width=2),
            marker=dict(size=8, color=self.colors['primary_orange']),
        ))

        fig.add_hline(y=r_bar, line_dash='solid',
                      line_color=self.colors['target_color'], line_width=2,
                      annotation_text='R-bar', annotation_position='right')
        fig.add_hline(y=ucl_r, line_dash='dash',
                      line_color=self.colors['ucl_color'], line_width=2,
                      annotation_text='UCL', annotation_position='right')

        if lcl_r > 0:
            fig.add_hline(y=lcl_r, line_dash='dash',
                          line_color=self.colors['lcl_color'], line_width=2,
                          annotation_text='LCL', annotation_position='right')

        fig.update_layout(
            title=f'{process_name} - Range Chart',
            xaxis_title='Batch Number',
            yaxis_title=f'Range ({process_unit})',
            **self.dark_template,
            hovermode='x unified',
            height=400,
            showlegend=True,
        )

        return fig


# ===== END OF FILE: utils/chart_utils.py =====
# This file creates all Plotly charts with dark theme and professional styling.
# Used by: app.py to generate interactive control charts for the UI.
