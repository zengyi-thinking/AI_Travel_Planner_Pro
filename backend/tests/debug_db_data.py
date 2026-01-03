"""
Debug script to check actual database data structure
"""
import sys
import os
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config.settings import settings
from app.modules.planner.models.itinerary import Itinerary
from sqlalchemy import select


async def check_itinerary_data():
    """Check the structure of itinerary data in the database"""

    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False
    )

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        # Get one itinerary
        result = await session.execute(
            select(Itinerary).where(Itinerary.id == 90)
        )
        itinerary = result.scalar_one_or_none()

        if not itinerary:
            print("Itinerary 90 not found!")
            return

        print("="*60)
        print("ITINERARY DATA STRUCTURE")
        print("="*60)

        print("\n1. Basic fields:")
        print(f"   ID: {itinerary.id}")
        print(f"   Title: {itinerary.title}")
        print(f"   Destination: {itinerary.destination}")
        print(f"   Departure: {itinerary.departure}")
        print(f"   Days: {itinerary.days}")
        print(f"   Budget: {itinerary.budget}")
        print(f"   Travel style: {itinerary.travel_style}")

        print("\n2. metadata_json:")
        if itinerary.metadata_json:
            import json
            for key, value in itinerary.metadata_json.items():
                print(f"   {key}: {type(value).__name__} = {value if not isinstance(value, (list, dict)) else f'[{type(value).__name__} with {len(value)} items]'}")
        else:
            print("   None")

        print("\n3. days_detail:")
        if itinerary.days_detail:
            for i, day in enumerate(itinerary.days_detail):
                print(f"   Day {i+1}:")
                print(f"      day_number: {day.day_number}")
                print(f"      title: {day.title}")
                print(f"      date: {day.date}")
                print(f"      activities type: {type(day.activities)}")
                if day.activities:
                    if isinstance(day.activities, list):
                        print(f"      activities: list with {len(day.activities)} items")
                        for j, act in enumerate(day.activities[:2]):  # Show first 2
                            print(f"         [{j}]: type={type(act).__name__}")
                    else:
                        print(f"      activities: {str(day.activities)[:100]}")

        print("\n" + "="*60)


if __name__ == "__main__":
    asyncio.run(check_itinerary_data())
