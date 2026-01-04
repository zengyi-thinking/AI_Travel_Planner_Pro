"""
PDF Export Service v2 - Match frontend styles
Creates PDF that looks exactly like the frontend preview
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


class PDFExportServiceV2:
    """Enhanced PDF export service matching frontend styles"""

    # Frontend color scheme
    COLORS = {
        'yellow_light': colors.HexColor('#fef9c3'),
        'yellow_dark': colors.HexColor('#fef08a'),
        'blue_light': colors.HexColor('#dbeafe'),
        'blue_dark': colors.HexColor('#bfdbfe'),
        'purple_light': colors.HexColor('#f3e8ff'),
        'purple_dark': colors.HexColor('#e9d5ff'),
        'orange_light': colors.HexColor('#fed7aa'),
        'orange_dark': colors.HexColor('#fdba74'),
        'teal': colors.HexColor('#14b8a6'),
        'teal_dark': colors.HexColor('#0d9488'),
        'text_primary': colors.HexColor('#1e293b'),
        'text_secondary': colors.HexColor('#475569'),
        'text_muted': colors.HexColor('#64748b'),
        'white': colors.whitesmoke,
    }

    def __init__(self):
        """Initialize PDF export service"""
        self.page_width, self.page_height = A4
        self.margin = 1.5 * cm

        # Register Chinese font
        try:
            pdfmetrics.registerFont(TTFont('SimSun', 'C:\\Windows\\Fonts\\simsun.ttc', subfontIndex=0))
            self.font_name = 'SimSun'
        except:
            logger.warning("Failed to register Chinese font, using default")
            self.font_name = 'Helvetica'

        self._setup_styles()

    def _setup_styles(self):
        """Setup PDF styles matching frontend"""
        self.styles = getSampleStyleSheet()

        # Title
        self.styles.add(ParagraphStyle(
            name='TitleCN',
            parent=self.styles['Title'],
            fontName=self.font_name,
            fontSize=28,
            textColor=self.COLORS['text_primary'],
            spaceAfter=20,
            alignment=TA_CENTER,
            leading=36
        ))

        # Section headers
        for name, color in [('Yellow', self.COLORS['text_primary']),
                            ('Blue', self.COLORS['text_primary']),
                            ('Purple', self.COLORS['text_primary']),
                            ('Orange', self.COLORS['text_primary'])]:
            self.styles.add(ParagraphStyle(
                name=f'Heading{name}',
                parent=self.styles['Heading2'],
                fontName=self.font_name,
                fontSize=16,
                textColor=color,
                spaceAfter=12,
                spaceBefore=10,
                leading=22
            ))

        # Body text
        self.styles.add(ParagraphStyle(
            name='BodyCN',
            parent=self.styles['BodyText'],
            fontName=self.font_name,
            fontSize=10,
            leading=14,
            textColor=self.COLORS['text_secondary'],
            spaceAfter=6
        ))

        # Highlight text
        self.styles.add(ParagraphStyle(
            name='Highlight',
            parent=self.styles['BodyText'],
            fontName=self.font_name,
            fontSize=9,
            leading=13,
            textColor=self.COLORS['text_secondary']
        ))

        # Small text
        self.styles.add(ParagraphStyle(
            name='SmallCN',
            parent=self.styles['BodyText'],
            fontName=self.font_name,
            fontSize=8,
            leading=11,
            textColor=self.COLORS['text_muted']
        ))

    def _safe_str(self, value: Any, default: str = '-') -> str:
        """Convert value to safe string"""
        if value is None:
            return default
        if isinstance(value, str):
            return value if value.strip() else default
        return str(value) if value else default

    def generate_itinerary_pdf(self, itinerary: Dict[str, Any]) -> bytes:
        """Generate PDF from itinerary data"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=self.margin,
            leftMargin=self.margin,
            topMargin=self.margin,
            bottomMargin=self.margin
        )

        story = self._build_content(itinerary)
        doc.build(story)

        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

    def _build_content(self, itinerary: Dict[str, Any]) -> list:
        """Build PDF content with frontend styling"""
        story = []

        # Title with logo
        story.append(Paragraph("✈️", self.styles['TitleCN']))
        story.append(Paragraph(itinerary.get('title', '旅行行程'), self.styles['TitleCN']))
        # Subtitle
        days = itinerary.get('days', 0)
        destination = itinerary.get('destination', '')
        departure = itinerary.get('departure', '')
        budget = itinerary.get('budget', 0)
        
        subtitle_parts = []
        if departure:
            subtitle_parts.append(f"{departure} → {destination}")
        else:
            subtitle_parts.append(destination)
        
        subtitle_parts.append(f"{days}天")
        subtitle_parts.append(f"预算¥{budget}")
        
        subtitle = " · ".join(subtitle_parts)
        story.append(Paragraph(subtitle, self.styles['SmallCN']))
        story.append(Spacer(1, 0.4*cm))
        
        # Divider line
        divider_data = [[""]]
        divider = Table(divider_data, colWidths=[self.page_width - 3*self.margin])
        divider.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.COLORS['teal']),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        story.append(divider)
        story.append(Spacer(1, 0.5*cm))

        # Overview Panel (Yellow)
        if self._has_overview_data(itinerary):
            story.extend(self._create_overview_panel(itinerary))

        # Preparation Panel (Blue)
        if self._has_preparation_data(itinerary):
            story.extend(self._create_preparation_panel(itinerary))

        # Daily Itinerary Panel (Purple)
        if itinerary.get('days_detail'):
            story.extend(self._create_days_panel(itinerary))

        # Tips Panel (Orange)
        if self._has_tips_data(itinerary):
            story.extend(self._create_tips_panel(itinerary))

        # Footer
        story.append(PageBreak())
        # Brand footer
        story.append(Paragraph("✈️ WanderFlow AI 智能规划助手", self.styles['SmallCN']))
        story.append(Spacer(1, 0.2*cm))
        
        # Generation date
        from datetime import datetime
        date_str = datetime.now().strftime("%Y年%m月%d日")
        story.append(Paragraph(f"生成于 {date_str}", self.styles['SmallCN']))

        return story

    def _has_overview_data(self, itinerary: Dict[str, Any]) -> bool:
        """Check if overview section has data"""
        return bool(
            itinerary.get('summary') or
            (itinerary.get('highlights') and len(itinerary['highlights'])) or
            itinerary.get('actual_cost') or
            itinerary.get('best_season') or
            itinerary.get('weather')
        )

    def _has_preparation_data(self, itinerary: Dict[str, Any]) -> bool:
        """Check if preparation section has data"""
        prep = itinerary.get('preparation', {})
        return bool(
            (prep.get('documents') and len(prep['documents'])) or
            (prep.get('essentials') and len(prep['essentials'])) or
            (prep.get('booking_reminders') and len(prep['booking_reminders']))
        )

    def _has_tips_data(self, itinerary: Dict[str, Any]) -> bool:
        """Check if tips section has data"""
        tips = itinerary.get('tips', {})
        return bool(
            tips.get('transportation') or tips.get('accommodation') or
            tips.get('food') or tips.get('shopping') or tips.get('safety') or
            (tips.get('other') and len(tips['other']))
        )

    def _create_overview_panel(self, itinerary: Dict[str, Any]) -> list:
        """Create overview panel with yellow gradient background"""
        content = []

        # Panel container table (for background color)
        panel_data = [[
            self._build_overview_content(itinerary)
        ]]

        panel_table = Table(panel_data, colWidths=[self.page_width - 3*self.margin])
        panel_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), self.COLORS['yellow_light']),
            ('LEFTPADDING', (0, 0), (0, 0), 12),
            ('RIGHTPADDING', (0, 0), (0, 0), 12),
            ('TOPPADDING', (0, 0), (0, 0), 12),
            ('BOTTOMPADDING', (0, 0), (0, 0), 12),
            ('VALIGN', (0, 0), (0, 0), 'TOP'),
        ]))

        content.append(panel_table)
        content.append(Spacer(1, 0.5*cm))
        return content

    def _build_overview_content(self, itinerary: Dict[str, Any]) -> list:
        """Build overview content"""
        content = []

        # Header
        header = Paragraph("行程概览", self.styles['HeadingYellow'])
        content.append(header)
        content.append(Spacer(1, 0.3*cm))

        # Summary
        if itinerary.get('summary'):
            summary_text = f"摘要：{itinerary['summary']}"
            content.append(Paragraph(summary_text, self.styles['BodyCN']))
            content.append(Spacer(1, 0.3*cm))

        # Highlights
        if itinerary.get('highlights') and len(itinerary['highlights']):
            content.append(Paragraph("亮点：", self.styles['BodyCN']))
            for idx, highlight in enumerate(itinerary['highlights'], 1):
                highlight_text = f"{idx}. {highlight}"
                content.append(Paragraph(highlight_text, self.styles['Highlight']))
            content.append(Spacer(1, 0.3*cm))

        # Cost comparison
        if itinerary.get('actual_cost'):
            budget = itinerary.get('budget', 0)
            actual = itinerary.get('actual_cost', 0)
            saved = budget - actual

            cost_text = f"预算：¥{budget} | 预计花费：¥{actual} | 节省：¥{saved}"
            content.append(Paragraph(cost_text, self.styles['BodyCN']))
            content.append(Spacer(1, 0.3*cm))

        # Best season and weather
        if itinerary.get('best_season'):
            content.append(Paragraph(f"最佳季节：{itinerary['best_season']}", self.styles['BodyCN']))
        if itinerary.get('weather'):
            content.append(Paragraph(f"天气提示：{itinerary['weather']}", self.styles['BodyCN']))

        return content

    def _create_preparation_panel(self, itinerary: Dict[str, Any]) -> list:
        """Create preparation panel with blue gradient background"""
        content = []
        prep = itinerary.get('preparation', {})

        # Panel container
        panel_data = [[
            self._build_preparation_content(prep)
        ]]

        panel_table = Table(panel_data, colWidths=[self.page_width - 3*self.margin])
        panel_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), self.COLORS['blue_light']),
            ('LEFTPADDING', (0, 0), (0, 0), 12),
            ('RIGHTPADDING', (0, 0), (0, 0), 12),
            ('TOPPADDING', (0, 0), (0, 0), 12),
            ('BOTTOMPADDING', (0, 0), (0, 0), 12),
            ('VALIGN', (0, 0), (0, 0), 'TOP'),
        ]))

        content.append(panel_table)
        content.append(Spacer(1, 0.5*cm))
        return content

    def _build_preparation_content(self, preparation: Dict[str, Any]) -> list:
        """Build preparation content"""
        content = []

        # Header
        content.append(Paragraph("行前准备", self.styles['HeadingBlue']))
        content.append(Spacer(1, 0.3*cm))

        # Documents
        if preparation.get('documents'):
            content.append(Paragraph("必备证件", self.styles['BodyCN']))
            for doc in preparation['documents']:
                content.append(Paragraph(f"  {doc}", self.styles['Highlight']))
            content.append(Spacer(1, 0.2*cm))

        # Essentials
        if preparation.get('essentials'):
            content.append(Paragraph("必备物品", self.styles['BodyCN']))
            for item in preparation['essentials']:
                content.append(Paragraph(f"  {item}", self.styles['Highlight']))
            content.append(Spacer(1, 0.2*cm))

        # Booking reminders
        if preparation.get('booking_reminders'):
            content.append(Paragraph("预订提醒", self.styles['BodyCN']))
            for reminder in preparation['booking_reminders']:
                content.append(Paragraph(f"  {reminder}", self.styles['Highlight']))

        return content

    def _create_days_panel(self, itinerary: Dict[str, Any]) -> list:
        """Create daily itinerary panel with purple gradient background"""
        content = []

        for day in itinerary.get('days_detail', []):
            day_content = self._create_day_section(day)
            content.extend(day_content)
            content.append(Spacer(1, 0.3*cm))

        return content

    def _create_day_section(self, day_plan: Dict[str, Any]) -> list:
        """Create single day section"""
        content = []

        # Panel container
        panel_data = [[
            self._build_day_content(day_plan)
        ]]

        panel_table = Table(panel_data, colWidths=[self.page_width - 3*self.margin])
        panel_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), self.COLORS['purple_light']),
            ('LEFTPADDING', (0, 0), (0, 0), 12),
            ('RIGHTPADDING', (0, 0), (0, 0), 12),
            ('TOPPADDING', (0, 0), (0, 0), 12),
            ('BOTTOMPADDING', (0, 0), (0, 0), 12),
            ('VALIGN', (0, 0), (0, 0), 'TOP'),
        ]))

        content.append(panel_table)
        return content

    def _build_day_content(self, day_plan: Dict[str, Any]) -> list:
        """Build day content"""
        content = []

        # Header with badge
        day_num = day_plan.get('day_number', 0)
        day_title = day_plan.get('title', '自由探索')

        content.append(Paragraph(f"第 {day_num} 天: {day_title}", self.styles['HeadingPurple']))
        content.append(Spacer(1, 0.3*cm))

        # Activities
        if day_plan.get('activities'):
            for activity in day_plan['activities']:
                time = self._safe_str(activity.get('time'), '--:--')
                title = self._safe_str(activity.get('title'), '活动')
                desc = self._safe_str(activity.get('description'), '')
                cost = activity.get('average_cost', 0)

                activity_text = f"{time} {title}"
                if desc:
                    activity_text += f"\n  {desc}"
                if cost:
                    activity_text += f" (¥{cost})"

                content.append(Paragraph(activity_text, self.styles['Highlight']))

        # Day cost
        if day_plan.get('total_cost'):
            content.append(Spacer(1, 0.2*cm))
            content.append(Paragraph(f"当日花费：¥{day_plan['total_cost']}", self.styles['SmallCN']))

        return content

    def _create_tips_panel(self, itinerary: Dict[str, Any]) -> list:
        """Create tips panel with orange gradient background"""
        content = []
        tips = itinerary.get('tips', {})

        # Panel container
        panel_data = [[
            self._build_tips_content(tips)
        ]]

        panel_table = Table(panel_data, colWidths=[self.page_width - 3*self.margin])
        panel_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), self.COLORS['orange_light']),
            ('LEFTPADDING', (0, 0), (0, 0), 12),
            ('RIGHTPADDING', (0, 0), (0, 0), 12),
            ('TOPPADDING', (0, 0), (0, 0), 12),
            ('BOTTOMPADDING', (0, 0), (0, 0), 12),
            ('VALIGN', (0, 0), (0, 0), 'TOP'),
        ]))

        content.append(panel_table)
        return content

    def _build_tips_content(self, tips: Dict[str, Any]) -> list:
        """Build tips content"""
        content = []

        # Header
        content.append(Paragraph("实用提示", self.styles['HeadingOrange']))
        content.append(Spacer(1, 0.3*cm))

        # Tip items
        tip_labels = {
            'transportation': '交通',
            'accommodation': '住宿',
            'food': '餐饮',
            'shopping': '购物',
            'safety': '安全'
        }

        for key, label in tip_labels.items():
            if tips.get(key):
                content.append(Paragraph(f"{label}：{tips[key]}", self.styles['BodyCN']))

        # Other tips
        if tips.get('other') and len(tips['other']):
            content.append(Spacer(1, 0.2*cm))
            content.append(Paragraph("其他提示：", self.styles['BodyCN']))
            for other_tip in tips['other']:
                content.append(Paragraph(f"  {other_tip}", self.styles['Highlight']))

        return content
