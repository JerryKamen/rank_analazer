"""
PDF Report Generator Module
Creates professional PDF reports with ranking coefficient results
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, 
    Spacer, PageBreak, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os
from typing import Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFReportGenerator:
    def __init__(self, output_dir: str = "reports"):
        """
        Initialize report generator
        
        Args:
            output_dir: Directory for output PDF files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_report(
        self,
        results: Dict,
        category_names: Dict[str, str],
        output_filename: str = "ranking_coefficient_report.pdf"
    ) -> str:
        """
        Generate PDF report with ranking coefficient results
        
        Args:
            results: Analysis results from RankingAnalyzer
            category_names: Mapping of category codes to friendly names
            output_filename: Name of output PDF file
            
        Returns:
            Path to generated PDF file
        """
        filepath = os.path.join(self.output_dir, output_filename)
        
        try:
            logger.info(f"Generating PDF report: {filepath}")
            
            # Create document
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=15*mm,
                leftMargin=15*mm,
                topMargin=15*mm,
                bottomMargin=15*mm
            )
            
            # Build story
            story = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=6,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            story.append(Paragraph("Ranking Koeficienty - MČR", title_style))
            
            # Subtitle
            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Normal'],
                fontSize=12,
                textColor=colors.HexColor('#666666'),
                spaceAfter=12,
                alignment=TA_CENTER
            )
            story.append(Paragraph(
                f"Dlouhá trať | {datetime.now().strftime('%d. %m. %Y')}",
                subtitle_style
            ))
            story.append(Spacer(1, 10*mm))
            
            # Results for each category
            for category, data in results.items():
                story.append(self._create_category_section(
                    category,
                    data,
                    category_names.get(category, category),
                    styles
                ))
            
            # Summary table
            story.append(PageBreak())
            story.append(Paragraph("Souhrn Koeficientů", title_style))
            story.append(Spacer(1, 5*mm))
            story.append(self._create_summary_table(results, category_names, styles))
            
            # Footer
            story.append(Spacer(1, 10*mm))
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#999999'),
                alignment=TA_CENTER
            )
            story.append(Paragraph(
                f"Vygenerováno: {datetime.now().strftime('%d. %m. %Y %H:%M:%S')}",
                footer_style
            ))
            
            # Build PDF
            doc.build(story)
            logger.info(f"PDF report generated successfully: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating PDF report: {e}")
            raise

    def _create_category_section(
        self,
        category_code: str,
        data: Dict,
        category_name: str,
        styles
    ) -> list:
        """
        Create section for one category
        
        Args:
            category_code: Category code (e.g., 'H21')
            data: Analysis data for this category
            category_name: Friendly category name
            styles: ReportLab styles
            
        Returns:
            List of story elements
        """
        story = []
        
        # Category heading
        heading_style = ParagraphStyle(
            'CategoryHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=6,
            fontName='Helvetica-Bold'
        )
        story.append(Paragraph(f"{category_code} - {category_name}", heading_style))
        
        # Coefficient box
        coefficient = data.get('coefficient', 0)
        status = data.get('status', 'UNKNOWN')
        
        if status == 'OK':
            coeff_text = f"<b>Koeficient:</b> {coefficient:.4f}"
            color = colors.HexColor('#27ae60')
        else:
            coeff_text = f"<b>Status:</b> {status}"
            color = colors.HexColor('#e74c3c')
        
        coeff_style = ParagraphStyle(
            'CoefficientBox',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#ffffff'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Create colored box for coefficient
        table_data = [[Paragraph(coeff_text, coeff_style)]]
        coeff_table = Table(table_data, colWidths=[150*mm])
        coeff_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), color),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(coeff_table)
        story.append(Spacer(1, 5*mm))
        
        # Top runners table
        if status == 'OK' and data.get('top_runners'):
            runners_heading = ParagraphStyle(
                'RunnersHeading',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor('#333333'),
                spaceAfter=3,
                fontName='Helvetica-Bold'
            )
            story.append(Paragraph("Nejlépe umístění běžci:", runners_heading))
            
            table_data = [['Pořadí', 'Jméno', 'Koeficient']]
            for runner in data['top_runners']:
                table_data.append([
                    str(runner['position']),
                    runner['name'],
                    f"{runner['coefficient']:.4f}"
                ])
            
            table = Table(table_data, colWidths=[20*mm, 100*mm, 30*mm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8f0f7')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffffff')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
                    colors.HexColor('#ffffff'),
                    colors.HexColor('#f9f9f9')
                ]),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ]))
            story.append(table)
        
        story.append(Spacer(1, 15*mm))
        return story

    def _create_summary_table(
        self,
        results: Dict,
        category_names: Dict[str, str],
        styles
    ):
        """
        Create summary table
        
        Args:
            results: Analysis results
            category_names: Category name mapping
            styles: ReportLab styles
            
        Returns:
            Table element
        """
        table_data = [['Kategorie', 'Koeficient', 'Běžců', 'Status']]
        
        for category, data in results.items():
            table_data.append([
                f"{category} - {category_names.get(category, category)}",
                f"{data.get('coefficient', 0):.4f}",
                str(data.get('runner_count', 0)),
                data.get('status', 'UNKNOWN')
            ])
        
        table = Table(table_data, colWidths=[70*mm, 35*mm, 20*mm, 30*mm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#ffffff')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffffff')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
                colors.HexColor('#ffffff'),
                colors.HexColor('#f9f9f9')
            ]),
            ('TOPPADDING', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        return table
