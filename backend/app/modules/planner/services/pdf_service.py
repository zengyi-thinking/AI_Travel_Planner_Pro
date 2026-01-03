"""
PDF Export Service for Travel Itineraries

This module handles PDF generation for travel itineraries.
"""

from io import BytesIO
from typing import Dict, Any, Optional
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether
)
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import logging

logger = logging.getLogger(__name__)


class PDFExportService:
    """Service for exporting travel itineraries to PDF"""

    def __init__(self):
        """Initialize PDF export service"""
        self.page_width, self.page_height = A4
        self.margin = 2 * cm

        # Register Chinese font (using system font)
        try:
            # Try to register a common Chinese font
            pdfmetrics.registerFont(TTFont('SimSun', 'C:\\Windows\\Fonts\\simsun.ttc', subfontIndex=0))
            self.font_name = 'SimSun'
        except:
            # Fallback to default font
            logger.warning("Failed to register Chinese font, using default")
            self.font_name = 'Helvetica'

        self._setup_styles()

    def _setup_styles(self):
        """Setup PDF styles"""
        self.styles = getSampleStyleSheet()

        # Custom styles
        self.styles.add(ParagraphStyle(
            name='TitleCN',
            parent=self.styles['Title'],
            fontName=self.font_name,
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))

        self.styles.add(ParagraphStyle(
            name='Heading1CN',
            parent=self.styles['Heading1'],
            fontName=self.font_name,
            fontSize=18,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=12,
            spaceBefore=20
        ))

        self.styles.add(ParagraphStyle(
            name='Heading2CN',
            parent=self.styles['Heading2'],
            fontName=self.font_name,
            fontSize=14,
            textColor=colors.HexColor('#7F8C8D'),
            spaceAfter=10,
            spaceBefore=15
        ))

        self.styles.add(ParagraphStyle(
            name='BodyCN',
            parent=self.styles['BodyText'],
            fontName=self.font_name,
            fontSize=10,
            leading=14,
            spaceAfter=8
        ))

        self.styles.add(ParagraphStyle(
            name='SmallCN',
            parent=self.styles['BodyText'],
            fontName=self.font_name,
            fontSize=9,
            leading=12,
            textColor=colors.HexColor('#7F8C8D')
        ))

        # Table cell style with word wrapping
        self.styles.add(ParagraphStyle(
            name='TableCell',
            parent=self.styles['BodyText'],
            fontName=self.font_name,
            fontSize=9,
            leading=12,
            wordWrap='CJK'
        ))

    def generate_itinerary_pdf(self, itinerary: Dict[str, Any]) -> bytes:
        """
        Generate PDF from itinerary data

        Args:
            itinerary: Itinerary data dictionary

        Returns:
            PDF file as bytes
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=self.margin,
            leftMargin=self.margin,
            topMargin=self.margin,
            bottomMargin=self.margin
        )

        # Build story (PDF content)
        story = []
        story = self._build_content(itinerary)

        # Generate PDF
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()

        return pdf_bytes

    def _build_content(self, itinerary: Dict[str, Any]) -> list:
        """Build PDF content from itinerary data"""
        story = []

        # Title
        title = itinerary.get('title', '旅行行程')
        story.append(Paragraph(title, self.styles['TitleCN']))
        story.append(Spacer(1, 0.5 * cm))

        # Basic info table
        story.append(self._create_basic_info_table(itinerary))
        story.append(Spacer(1, 0.5 * cm))

        # Summary
        if itinerary.get('summary'):
            story.append(Paragraph("行程概述", self.styles['Heading1CN']))
            story.append(Paragraph(itinerary['summary'], self.styles['BodyCN']))
            story.append(Spacer(1, 0.3 * cm))

        # Highlights
        if itinerary.get('highlights'):
            story.append(Paragraph("行程亮点", self.styles['Heading1CN']))
            for highlight in itinerary['highlights']:
                story.append(Paragraph(f"• {highlight}", self.styles['BodyCN']))
            story.append(Spacer(1, 0.3 * cm))

        # Daily itinerary
        if itinerary.get('days_detail'):
            story.append(Paragraph("详细行程", self.styles['Heading1CN']))
            story.append(Spacer(1, 0.3 * cm))

            for day_plan in itinerary['days_detail']:
                day_content = self._create_day_section(day_plan)
                story.extend(day_content)
                story.append(Spacer(1, 0.3 * cm))

        # Cost breakdown
        if itinerary.get('cost_breakdown'):
            story.append(PageBreak())
            story.append(Paragraph("费用明细", self.styles['Heading1CN']))
            story.append(self._create_cost_table(itinerary['cost_breakdown']))
            story.append(Spacer(1, 0.3 * cm))

            if itinerary.get('actual_cost'):
                story.append(Paragraph(
                    f"总花费: ¥{itinerary['actual_cost']}",
                    self.styles['Heading2CN']
                ))

        # Preparation
        if itinerary.get('preparation'):
            story.append(PageBreak())
            story.append(Paragraph("行前准备", self.styles['Heading1CN']))
            story.extend(self._create_preparation_section(itinerary['preparation']))
            story.append(Spacer(1, 0.3 * cm))

        # Tips
        if itinerary.get('tips'):
            story.append(Paragraph("实用提示", self.styles['Heading1CN']))
            story.extend(self._create_tips_section(itinerary['tips']))

        # Footer
        story.append(PageBreak())
        story.append(Paragraph(
            "本行程由 WanderFlow AI 智能规划助手生成",
            self.styles['SmallCN']
        ))

        return story

    def _create_basic_info_table(self, itinerary: Dict[str, Any]) -> Table:
        """Create basic information table"""
        data = [
            [Paragraph('目的地:', self.styles['BodyCN']), Paragraph(self._safe_str(itinerary.get('destination')), self.styles['TableCell'])],
            [Paragraph('出发地:', self.styles['BodyCN']), Paragraph(self._safe_str(itinerary.get('departure'), '未指定'), self.styles['TableCell'])],
            [Paragraph('天数:', self.styles['BodyCN']), Paragraph(f"{itinerary.get('days', 0)} 天", self.styles['TableCell'])],
            [Paragraph('预算:', self.styles['BodyCN']), Paragraph(f"¥{itinerary.get('budget', 0)}", self.styles['TableCell'])],
            [Paragraph('旅行风格:', self.styles['BodyCN']), Paragraph(self._get_travel_style_label(itinerary.get('travel_style', 'leisure')), self.styles['TableCell'])],
        ]

        table = Table(data, colWidths=[4*cm, 10*cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), self.font_name),
            ('FONTNAME', (1, 0), (1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        return table

    def _create_day_section(self, day_plan: Dict[str, Any]) -> list:
        """Create day section content"""
        content = []

        # Day header
        day_title = f"第 {day_plan.get('day_number', 0)} 天: {day_plan.get('title', '')}"
        content.append(Paragraph(day_title, self.styles['Heading2CN']))

        # Date
        if day_plan.get('date'):
            content.append(Paragraph(f"日期: {day_plan['date']}", self.styles['SmallCN']))

        # Summary
        if day_plan.get('summary'):
            content.append(Paragraph(day_plan['summary'], self.styles['BodyCN']))

        # Activities
        if day_plan.get('activities'):
            activities_data = [
                [Paragraph('时间', self.styles['BodyCN']), Paragraph('活动', self.styles['BodyCN']), Paragraph('描述', self.styles['BodyCN']), Paragraph('费用', self.styles['BodyCN'])]
            ]
            for activity in day_plan['activities']:
                activities_data.append([
                    Paragraph(self._safe_str(activity.get('time')), self.styles['TableCell']),
                    Paragraph(self._safe_str(activity.get('title')), self.styles['TableCell']),
                    Paragraph(self._safe_str(activity.get('description')), self.styles['TableCell']),
                    Paragraph(f"¥{activity.get('average_cost', 0)}", self.styles['TableCell'])
                ])

            activities_table = Table(activities_data, colWidths=[2.5*cm, 3.5*cm, 5*cm, 2*cm])
            activities_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), self.font_name),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            content.append(activities_table)

        # Day cost
        if day_plan.get('total_cost'):
            content.append(Spacer(1, 0.2 * cm))
            content.append(Paragraph(
                f"当日花费: ¥{day_plan['total_cost']}",
                self.styles['SmallCN']
            ))

        return content

    def _create_cost_table(self, cost_breakdown: Dict[str, Any]) -> Table:
        """Create cost breakdown table"""
        data = [
            [Paragraph('项目', self.styles['BodyCN']), Paragraph('金额', self.styles['BodyCN'])],
            [Paragraph('交通', self.styles['TableCell']), Paragraph(f"¥{cost_breakdown.get('transportation', 0)}", self.styles['TableCell'])],
            [Paragraph('住宿', self.styles['TableCell']), Paragraph(f"¥{cost_breakdown.get('accommodation', 0)}", self.styles['TableCell'])],
            [Paragraph('餐饮', self.styles['TableCell']), Paragraph(f"¥{cost_breakdown.get('food', 0)}", self.styles['TableCell'])],
            [Paragraph('门票', self.styles['TableCell']), Paragraph(f"¥{cost_breakdown.get('tickets', 0)}", self.styles['TableCell'])],
            [Paragraph('购物', self.styles['TableCell']), Paragraph(f"¥{cost_breakdown.get('shopping', 0)}", self.styles['TableCell'])],
            [Paragraph('其他', self.styles['TableCell']), Paragraph(f"¥{cost_breakdown.get('other', 0)}", self.styles['TableCell'])],
        ]

        table = Table(data, colWidths=[8*cm, 6*cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27AE60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        return table

    def _create_preparation_section(self, preparation: Dict[str, Any]) -> list:
        """Create preparation section"""
        content = []

        sections = [
            ('必备证件', preparation.get('documents', [])),
            ('必带物品', preparation.get('essentials', [])),
            ('建议携带', preparation.get('suggestions', [])),
            ('预订提醒', preparation.get('booking_reminders', [])),
        ]

        for title, items in sections:
            if items:
                content.append(Paragraph(title, self.styles['Heading2CN']))
                for item in items:
                    content.append(Paragraph(f"• {item}", self.styles['BodyCN']))
                content.append(Spacer(1, 0.2 * cm))

        return content

    def _create_tips_section(self, tips: Dict[str, Any]) -> list:
        """Create tips section"""
        content = []

        tip_items = [
            ('交通', tips.get('transportation')),
            ('住宿', tips.get('accommodation')),
            ('餐饮', tips.get('food')),
            ('购物', tips.get('shopping')),
            ('安全', tips.get('safety')),
        ]

        for title, tip in tip_items:
            if tip:
                content.append(Paragraph(f"{title}提示", self.styles['Heading2CN']))
                content.append(Paragraph(tip, self.styles['BodyCN']))
                content.append(Spacer(1, 0.2 * cm))

        if tips.get('other'):
            content.append(Paragraph("其他提醒", self.styles['Heading2CN']))
            for other_tip in tips['other']:
                content.append(Paragraph(f"• {other_tip}", self.styles['BodyCN']))

        return content

    def _safe_str(self, value: Any, default: str = '-') -> str:
        """Convert value to safe string, handle None and non-string values"""
        if value is None:
            return default
        if isinstance(value, str):
            return value if value.strip() else default
        return str(value) if value else default

    def _get_travel_style_label(self, style: str) -> str:
        """Get travel style label"""
        style_map = {
            'leisure': '休闲游',
            'adventure': '冒险游',
            'foodie': '美食游',
            'cultural': '文化游'
        }
        return style_map.get(style, style)
