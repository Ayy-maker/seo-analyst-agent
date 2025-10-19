"""
PDF styling utilities for professional reports
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)


class PDFStyles:
    """Professional PDF styling matching the HTML design"""
    
    # Color palette (matching HTML design)
    COLORS = {
        'primary': colors.HexColor('#667eea'),
        'secondary': colors.HexColor('#764ba2'),
        'success': colors.HexColor('#48bb78'),
        'warning': colors.HexColor('#f39c12'),
        'danger': colors.HexColor('#dc2626'),
        'gray': colors.HexColor('#718096'),
        'dark_gray': colors.HexColor('#2d3748'),
        'light_gray': colors.HexColor('#e2e8f0'),
        'white': colors.white,
        'bg_gradient_start': colors.HexColor('#f5f7fa'),
        'bg_gradient_end': colors.HexColor('#c3cfe2'),
    }
    
    @staticmethod
    def get_styles():
        """Get custom paragraph styles for the report"""
        styles = getSampleStyleSheet()
        
        # Custom styles
        custom_styles = {
            'CustomTitle': ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=36,
                textColor=PDFStyles.COLORS['white'],
                alignment=TA_CENTER,
                spaceAfter=12,
                fontName='Helvetica-Bold',
                leading=42
            ),
            'CustomSubtitle': ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Normal'],
                fontSize=18,
                textColor=PDFStyles.COLORS['white'],
                alignment=TA_CENTER,
                spaceAfter=20,
                fontName='Helvetica',
                leading=22
            ),
            'SectionHeader': ParagraphStyle(
                'SectionHeader',
                parent=styles['Heading2'],
                fontSize=24,
                textColor=PDFStyles.COLORS['dark_gray'],
                spaceBefore=30,
                spaceAfter=15,
                fontName='Helvetica-Bold',
                leading=28
            ),
            'SubsectionHeader': ParagraphStyle(
                'SubsectionHeader',
                parent=styles['Heading3'],
                fontSize=18,
                textColor=PDFStyles.COLORS['dark_gray'],
                spaceBefore=20,
                spaceAfter=10,
                fontName='Helvetica-Bold',
                leading=22
            ),
            'ReportBody': ParagraphStyle(
                'ReportBody',
                parent=styles['Normal'],
                fontSize=11,
                textColor=PDFStyles.COLORS['dark_gray'],
                alignment=TA_JUSTIFY,
                spaceAfter=12,
                leading=16
            ),
            'ReportBullet': ParagraphStyle(
                'ReportBullet',
                parent=styles['Normal'],
                fontSize=10,
                textColor=PDFStyles.COLORS['dark_gray'],
                leftIndent=20,
                spaceAfter=8,
                leading=14
            ),
            'TableHeader': ParagraphStyle(
                'TableHeader',
                parent=styles['Normal'],
                fontSize=10,
                textColor=PDFStyles.COLORS['white'],
                fontName='Helvetica-Bold',
                alignment=TA_LEFT
            ),
            'TableCell': ParagraphStyle(
                'TableCell',
                parent=styles['Normal'],
                fontSize=9,
                textColor=PDFStyles.COLORS['dark_gray'],
                alignment=TA_LEFT
            ),
            'FooterText': ParagraphStyle(
                'FooterText',
                parent=styles['Normal'],
                fontSize=8,
                textColor=PDFStyles.COLORS['gray'],
                alignment=TA_CENTER
            )
        }
        
        # Add custom styles to stylesheet
        for name, style in custom_styles.items():
            styles.add(style)
        
        return styles
    
    @staticmethod
    def create_gradient_table_style(num_cols):
        """Create professional table style with gradient header"""
        return TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), PDFStyles.COLORS['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), PDFStyles.COLORS['white']),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Body styling
            ('BACKGROUND', (0, 1), (-1, -1), PDFStyles.COLORS['white']),
            ('TEXTCOLOR', (0, 1), (-1, -1), PDFStyles.COLORS['dark_gray']),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 10),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, PDFStyles.COLORS['light_gray']),
            ('BOX', (0, 0), (-1, -1), 1, PDFStyles.COLORS['primary']),
            
            # Alternating rows
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), 
             [PDFStyles.COLORS['white'], PDFStyles.COLORS['bg_gradient_start']]),
        ])
    
    @staticmethod
    def create_kpi_box_style():
        """Create style for KPI boxes"""
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), PDFStyles.COLORS['white']),
            ('BOX', (0, 0), (-1, -1), 3, PDFStyles.COLORS['primary']),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ])
    
    @staticmethod
    def create_recommendation_box_style():
        """Create style for recommendation boxes"""
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f39c1215')),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
            ('LINEBELOW', (0, 0), (0, -1), 5, PDFStyles.COLORS['warning']),
        ])
    
    @staticmethod
    def add_gradient_header(canvas_obj, doc, title, subtitle, date, logo_img=None):
        """Draw stunning gradient header on first page with optional logo"""
        canvas_obj.saveState()
        
        # Gradient background (simulate with rectangles)
        width, height = letter
        header_height = 3 * inch
        
        # Draw beautiful gradient (blue-purple)
        gradient_steps = 60
        for i in range(gradient_steps):
            progress = i / gradient_steps
            # Blend from primary to secondary
            r = 0.40 + (0.46 - 0.40) * progress
            g = 0.49 - (0.49 - 0.29) * progress
            b = 0.92 - (0.92 - 0.64) * progress
            alpha = 1.0 - (progress * 0.15)
            
            canvas_obj.setFillColorRGB(r, g, b, alpha=alpha)
            rect_height = header_height / gradient_steps
            canvas_obj.rect(0, height - (i * rect_height) - rect_height, 
                          width, rect_height, fill=True, stroke=False)
        
        # Add decorative circle patterns
        canvas_obj.setFillColorRGB(1, 1, 1, alpha=0.05)
        canvas_obj.circle(width * 0.15, height - 0.8*inch, 1.5*inch, fill=True, stroke=False)
        canvas_obj.circle(width * 0.85, height - 2*inch, 2*inch, fill=True, stroke=False)
        
        # Title with shadow effect
        canvas_obj.setFillColorRGB(0, 0, 0, alpha=0.2)
        canvas_obj.setFont('Helvetica-Bold', 42)
        canvas_obj.drawCentredString(width/2 + 2, height - 1.15*inch - 2, title)
        
        canvas_obj.setFillColor(PDFStyles.COLORS['white'])
        canvas_obj.setFont('Helvetica-Bold', 42)
        canvas_obj.drawCentredString(width/2, height - 1.15*inch, title)
        
        # Subtitle
        canvas_obj.setFillColorRGB(1, 1, 1, alpha=0.9)
        canvas_obj.setFont('Helvetica', 20)
        canvas_obj.drawCentredString(width/2, height - 1.65*inch, subtitle)
        
        # Date badge with background
        badge_width = 3.5*inch
        badge_height = 0.5*inch
        badge_x = width/2 - badge_width/2
        badge_y = height - 2.3*inch
        
        # Badge shadow
        canvas_obj.setFillColorRGB(0, 0, 0, alpha=0.1)
        canvas_obj.roundRect(badge_x + 2, badge_y - 2, 
                            badge_width, badge_height, 0.25*inch,
                            fill=True, stroke=False)
        
        # Badge background
        canvas_obj.setFillColorRGB(1, 1, 1, alpha=0.25)
        canvas_obj.roundRect(badge_x, badge_y, 
                            badge_width, badge_height, 0.25*inch,
                            fill=True, stroke=False)
        
        # Badge border
        canvas_obj.setStrokeColorRGB(1, 1, 1, alpha=0.5)
        canvas_obj.setLineWidth(2)
        canvas_obj.roundRect(badge_x, badge_y, 
                            badge_width, badge_height, 0.25*inch,
                            fill=False, stroke=True)
        
        # Badge text
        canvas_obj.setFillColor(PDFStyles.COLORS['white'])
        canvas_obj.setFont('Helvetica-Bold', 11)
        canvas_obj.drawCentredString(width/2, badge_y + 0.18*inch, date)
        
        # Add logo if provided
        if logo_img:
            from reportlab.platypus import Image as RLImage
            try:
                # Position logo in top-right corner
                logo = RLImage(logo_img, width=1.5*inch, height=0.6*inch)
                logo.drawOn(canvas_obj, width - 2*inch, height - 0.9*inch)
            except:
                pass  # If logo fails, continue without it
        
        canvas_obj.restoreState()
    
    @staticmethod
    def add_footer(canvas_obj, doc, company_name, report_date):
        """Add footer to pages"""
        canvas_obj.saveState()
        
        width, height = letter
        
        # Footer background
        canvas_obj.setFillColor(PDFStyles.COLORS['dark_gray'])
        canvas_obj.rect(0, 0, width, 0.8*inch, fill=True, stroke=False)
        
        # Footer text
        canvas_obj.setFillColor(PDFStyles.COLORS['white'])
        canvas_obj.setFont('Helvetica-Bold', 12)
        canvas_obj.drawCentredString(width/2, 0.55*inch, company_name)
        
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.setFillColor(colors.HexColor('#a0aec0'))
        canvas_obj.drawCentredString(width/2, 0.4*inch, f"Report Generated: {report_date}")
        
        # Page number
        canvas_obj.setFont('Helvetica', 8)
        page_num = canvas_obj.getPageNumber()
        canvas_obj.drawRightString(width - 0.5*inch, 0.4*inch, f"Page {page_num}")
        
        canvas_obj.restoreState()
