"""
Simple PDF generation test to debug the issue
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors


def test_simple_pdf():
    """Test simple PDF generation"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    story = []

    # Add a simple title
    story.append(Paragraph("Test PDF", getSampleStyleSheet()['Title']))
    story.append(Spacer(1, 1*cm))

    # Add some text
    story.append(Paragraph("This is a simple PDF test document", getSampleStyleSheet()['BodyText']))

    try:
        doc.build(story)
        pdf_bytes = buffer.getvalue()

        # Save to file
        with open('test_output.pdf', 'wb') as f:
            f.write(pdf_bytes)

        print("[OK] Simple PDF generated successfully!")
        print(f"PDF size: {len(pdf_bytes)} bytes")
        return True
    except Exception as e:
        print(f"[FAIL] PDF generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_complex_pdf():
    """Test PDF with tables"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    story = []

    # Title
    story.append(Paragraph("Itinerary Test PDF", getSampleStyleSheet()['Title']))
    story.append(Spacer(1, 1*cm))

    # Table
    data = [
        ['Item', 'Content'],
        ['Destination', 'Harbin'],
        ['Days', '3 days'],
        ['Budget', '5000 yuan']
    ]

    table = Table(data, colWidths=[4*cm, 6*cm])
    story.append(table)
    story.append(Spacer(1, 1*cm))

    try:
        doc.build(story)
        pdf_bytes = buffer.getvalue()

        with open('test_table_output.pdf', 'wb') as f:
            f.write(pdf_bytes)

        print("[OK] PDF with table generated successfully!")
        print(f"PDF size: {len(pdf_bytes)} bytes")
        return True
    except Exception as e:
        print(f"[FAIL] PDF with table generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_list_content():
    """Test PDF with list content (like our real data)"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    story = []

    # Title
    story.append(Paragraph("List Content Test", getSampleStyleSheet()['Title']))
    story.append(Spacer(1, 1*cm))

    # Add list items directly (not extend)
    story.append(Paragraph("Item 1: Test item 1", getSampleStyleSheet()['BodyText']))
    story.append(Paragraph("Item 2: Test item 2", getSampleStyleSheet()['BodyText']))
    story.append(Spacer(1, 1*cm))

    # Table
    data = [['Title', 'Content']]
    data.append(['Activity 1', 'Visit Central Street'])
    data.append(['Activity 2', 'Visit Saint Sophia Cathedral'])

    table = Table(data, colWidths=[4*cm, 6*cm])
    story.append(table)

    try:
        doc.build(story)
        pdf_bytes = buffer.getvalue()

        with open('test_list_output.pdf', 'wb') as f:
            f.write(pdf_bytes)

        print("[OK] PDF with list content generated successfully!")
        print(f"PDF size: {len(pdf_bytes)} bytes")
        return True
    except Exception as e:
        print(f"[FAIL] PDF with list content generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("="*60)
    print("PDF Generation Tests")
    print("="*60)

    print("\nTest 1: Simple PDF")
    test_simple_pdf()

    print("\nTest 2: PDF with table")
    test_complex_pdf()

    print("\nTest 3: PDF with list content (simulating real data)")
    test_list_content()

    print("\nAll tests completed!")
