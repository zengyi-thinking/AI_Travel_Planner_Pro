"""
Test PDF service with real itinerary data structure
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from io import BytesIO
from app.modules.planner.services.pdf_service import PDFExportService


def test_pdf_service():
    """Test PDF service with sample data"""
    # Create sample itinerary data (matching real structure)
    sample_itinerary = {
        'id': 1,
        'title': 'Harbin Ice Festival Trip',
        'destination': 'Harbin',
        'departure': 'Beijing',
        'days': 3,
        'budget': 5000,
        'travel_style': 'leisure',
        'summary': 'Experience the magical Ice and Snow Festival in Harbin',
        'highlights': [
            'Ice and Snow World',
            'Saint Sophia Cathedral',
            'Central Street',
            'Sun Island Snow Sculpture Art Expo'
        ],
        'days_detail': [
            {
                'day_number': 1,
                'title': 'Arrival and City Exploration',
                'date': '2025-01-15',
                'summary': 'Arrive in Harbin and explore the city center',
                'activities': [
                    {
                        'time': '09:00',
                        'title': 'Arrival in Harbin',
                        'description': 'Fly from Beijing to Harbin, transfer to hotel',
                        'average_cost': 500
                    },
                    {
                        'time': '14:00',
                        'title': 'Central Street',
                        'description': 'Walk along the historic Central Street',
                        'average_cost': 0
                    },
                    {
                        'time': '18:00',
                        'title': 'Dinner at Local Restaurant',
                        'description': 'Try Harbin-style Russian cuisine',
                        'average_cost': 150
                    }
                ],
                'total_cost': 650
            },
            {
                'day_number': 2,
                'title': 'Ice Festival Day',
                'date': '2025-01-16',
                'summary': 'Full day at Ice and Snow World',
                'activities': [
                    {
                        'time': '10:00',
                        'title': 'Ice and Snow World',
                        'description': 'Explore magnificent ice sculptures',
                        'average_cost': 330
                    },
                    {
                        'time': '15:00',
                        'title': 'Sun Island',
                        'description': 'Visit snow sculpture art expo',
                        'average_cost': 240
                    }
                ],
                'total_cost': 570
            }
        ],
        'cost_breakdown': {
            'transportation': 1000,
            'accommodation': 1200,
            'food': 800,
            'tickets': 570,
            'shopping': 300,
            'other': 200
        },
        'actual_cost': 4070,
        'preparation': {
            'documents': ['ID card', 'Flight tickets'],
            'essentials': ['Warm clothes', 'Camera', 'Power bank'],
            'suggestions': ['Buy thermal underwear', 'Download offline maps'],
            'booking_reminders': ['Book hotel in advance', 'Reserve flight tickets early']
        },
        'tips': {
            'transportation': 'Use taxi or地铁 for city transport',
            'accommodation': 'Stay near Central Street for convenience',
            'food': 'Try Russian-style bread and sausages',
            'shopping': 'Buy Russian souvenirs on Central Street',
            'safety': 'Be careful of icy roads',
            'other': ['Bring hand warmers', 'Keep phone battery charged in cold']
        }
    }

    print("="*60)
    print("Testing PDF Export Service")
    print("="*60)

    try:
        # Create PDF service
        pdf_service = PDFExportService()
        print("[OK] PDF service initialized successfully")

        # Generate PDF
        print("\nGenerating PDF from itinerary data...")
        pdf_bytes = pdf_service.generate_itinerary_pdf(sample_itinerary)

        # Save to file
        output_path = 'test_itinerary_output.pdf'
        with open(output_path, 'wb') as f:
            f.write(pdf_bytes)

        print(f"[OK] PDF generated successfully!")
        print(f"PDF size: {len(pdf_bytes)} bytes")
        print(f"Saved to: {output_path}")
        return True

    except Exception as e:
        print(f"[FAIL] PDF generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_pdf_service()
    print("\n" + "="*60)
    if success:
        print("TEST PASSED - PDF export working correctly!")
    else:
        print("TEST FAILED - Check errors above")
    print("="*60)
