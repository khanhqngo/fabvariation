"""
=== utils/pdf_generator.py ===

This module generates professional PDF reports for SPC analysis using ReportLab.
Creates PDF documents with:
- Micron-style branding and headers
- Control chart images
- Alert/violation tables
- Summary statistics
- Scrap cost analysis
- Timestamp and metadata
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from typing import List, Dict
import io
import plotly.graph_objects as go


class PDFReportGenerator:
    """
    Generates professional PDF reports for SPC analysis.
    """

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._add_custom_styles()

    def _add_custom_styles(self):
        """Add custom paragraph styles for the report."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#00CC66'),
            spaceAfter=12,
            alignment=TA_CENTER,
        ))

        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#FF6600'),
            spaceBefore=12,
            spaceAfter=6,
        ))

        # Body style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
        ))

    def generate_report(
        self,
        filepath: str,
        process_name: str,
        process_unit: str,
        chart_figures: List[go.Figure],
        violations: List[Dict],
        summary_stats: Dict,
        scrap_cost: float,
        simulation_metadata: Dict
    ) -> None:
        """
        Generate complete PDF report.

        Args:
            filepath: Output PDF file path
            process_name: Name of the process
            process_unit: Unit of measurement
            chart_figures: List of Plotly figures to include
            violations: List of violation dictionaries
            summary_stats: Summary statistics dictionary
            scrap_cost: Estimated scrap cost
            simulation_metadata: Simulation metadata (drift scenario, etc.)
        """
        # Create PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
        )

        # Container for PDF elements
        story = []

        # Add header
        story.extend(self._create_header(process_name))

        # Add metadata section
        story.extend(self._create_metadata_section(simulation_metadata))

        # Add summary statistics
        story.extend(self._create_summary_section(summary_stats, process_unit))

        # Add scrap cost analysis
        story.extend(self._create_cost_section(scrap_cost, len(violations)))

        # Add violation alerts
        story.extend(self._create_violations_section(violations))

        # Add chart images
        story.extend(self._create_charts_section(chart_figures))

        # Add footer
        story.extend(self._create_footer())

        # Build PDF
        doc.build(story)

    def _create_header(self, process_name: str) -> List:
        """Create report header with branding."""
        elements = []

        # Title
        title = Paragraph(
            'FabVariation SPC Report',
            self.styles['CustomTitle']
        )
        elements.append(title)

        # Subtitle
        subtitle = Paragraph(
            f'Process: {process_name}',
            self.styles['CustomHeading']
        )
        elements.append(subtitle)

        # Timestamp
        timestamp = Paragraph(
            f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            self.styles['CustomBody']
        )
        elements.append(timestamp)

        elements.append(Spacer(1, 0.3*inch))

        return elements

    def _create_metadata_section(self, metadata: Dict) -> List:
        """Create metadata section."""
        elements = []

        heading = Paragraph('Simulation Details', self.styles['CustomHeading'])
        elements.append(heading)

        data = [
            ['Drift Scenario:', metadata.get('drift_scenario', 'N/A')],
            ['Target Mean:', f"{metadata.get('target_mean', 0):.2f}"],
            ['Target Sigma:', f"{metadata.get('target_sigma', 0):.2f}"],
            ['Sample Size:', str(metadata.get('sample_size', 0))],
            ['Number of Batches:', str(metadata.get('num_batches', 0))],
        ]

        table = Table(data, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#2E3440')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))

        return elements

    def _create_summary_section(self, stats: Dict, unit: str) -> List:
        """Create summary statistics section."""
        elements = []

        heading = Paragraph('Summary Statistics', self.styles['CustomHeading'])
        elements.append(heading)

        data = [
            ['Metric', 'Value'],
            ['Overall Mean', f"{stats.get('overall_mean', 0):.2f} {unit}"],
            ['Overall Std Dev', f"{stats.get('overall_std', 0):.2f} {unit}"],
            ['Minimum', f"{stats.get('overall_min', 0):.2f} {unit}"],
            ['Maximum', f"{stats.get('overall_max', 0):.2f} {unit}"],
            ['Total Measurements', str(stats.get('total_measurements', 0))],
        ]

        table = Table(data, colWidths=[2.5*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00CC66')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F0F0')]),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))

        return elements

    def _create_cost_section(self, scrap_cost: float, num_violations: int) -> List:
        """Create scrap cost analysis section."""
        elements = []

        heading = Paragraph('Scrap Cost Analysis', self.styles['CustomHeading'])
        elements.append(heading)

        cost_color = colors.HexColor('#FF0066') if num_violations > 0 else colors.HexColor('#00CC66')

        data = [
            ['Out-of-Control Points Detected:', str(num_violations)],
            ['Estimated Scrap Cost:', f'${scrap_cost:,.2f}'],
        ]

        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#2E3440')),
            ('BACKGROUND', (1, 1), (1, 1), cost_color),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))

        return elements

    def _create_violations_section(self, violations: List[Dict]) -> List:
        """Create violations/alerts section."""
        elements = []

        heading = Paragraph(
            f'Control Chart Violations ({len(violations)} detected)',
            self.styles['CustomHeading']
        )
        elements.append(heading)

        if not violations:
            no_violations = Paragraph(
                'No violations detected - Process is in control.',
                self.styles['CustomBody']
            )
            elements.append(no_violations)
        else:
            # Create table header
            data = [['Batch', 'Rule', 'Description', 'Severity']]

            # Add violation rows (limit to first 20 for space)
            for v in violations[:20]:
                data.append([
                    str(v['batch']),
                    v['rule'],
                    v['description'],
                    v['severity'].upper(),
                ])

            if len(violations) > 20:
                data.append(['...', '...', f'{len(violations) - 20} more violations', '...'])

            table = Table(data, colWidths=[0.7*inch, 1.5*inch, 3*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF6600')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFF5F5')]),
            ]))

            elements.append(table)

        elements.append(Spacer(1, 0.3*inch))

        return elements

    def _create_charts_section(self, figures: List[go.Figure]) -> List:
        """Create charts section with embedded images."""
        elements = []

        heading = Paragraph('Control Charts', self.styles['CustomHeading'])
        elements.append(heading)

        for fig in figures:
            # Convert Plotly figure to image bytes
            img_bytes = fig.to_image(format='png', width=800, height=400, scale=2)

            # Create ReportLab Image
            img = Image(io.BytesIO(img_bytes), width=6.5*inch, height=3.25*inch)
            elements.append(img)
            elements.append(Spacer(1, 0.2*inch))

        return elements

    def _create_footer(self) -> List:
        """Create report footer."""
        elements = []

        elements.append(Spacer(1, 0.3*inch))

        footer_text = Paragraph(
            'This report was generated by FabVariation - Real-Time Process Variation Simulator & Excursion Preventer<br/>'
            'For use in semiconductor manufacturing process control and quality assurance.',
            ParagraphStyle(
                name='Footer',
                fontSize=8,
                textColor=colors.grey,
                alignment=TA_CENTER,
            )
        )
        elements.append(footer_text)

        return elements


# ===== END OF FILE: utils/pdf_generator.py =====
# This file generates professional PDF reports with charts and statistics.
# Used by: app.py when user clicks "Export PDF Report" button.
