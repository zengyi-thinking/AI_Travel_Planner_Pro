"""
Travel Planner Agent

This module contains the AI agent responsible for generating travel itineraries.
It uses LLM to create intelligent, personalized travel plans.
"""

from typing import List, Dict, Any
from app.core.ai.factory import LLMFactory
from app.core.config import settings
from langchain.schema import HumanMessage, SystemMessage
from app.modules.planner.prompts.planning_prompts import PLANNING_SYSTEM_PROMPT
import logging

logger = logging.getLogger(__name__)


class TravelPlannerAgent:
    """
    AI agent for travel planning.
    Generates intelligent travel itineraries based on user preferences.
    """

    def __init__(self):
        """Initialize the planner agent."""
        self.llm = LLMFactory.create_client(
            provider="openai",
            temperature=settings.AI_TEMPERATURE
        )

    async def generate_itinerary(
        self,
        destination: str,
        days: int,
        budget: float,
        travel_style: str,
        departure: str = None,
        preferences: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Generate a travel itinerary using AI.

        Args:
            destination: Travel destination
            days: Number of days
            budget: Budget in CNY
            travel_style: Travel style (leisure, adventure, foodie)
            departure: Departure location
            preferences: Additional preferences

        Returns:
            Generated itinerary data
        """
        # Prepare user input
        user_input = f"""
        Destination: {destination}
        Departure: {departure or 'Not specified'}
        Days: {days}
        Budget: ¥{budget}
        Travel Style: {travel_style}
        Preferences: {preferences or 'None specified'}
        """

        # Generate itinerary
        messages = [
            SystemMessage(content=PLANNING_SYSTEM_PROMPT),
            HumanMessage(content=user_input)
        ]

        try:
            response = await LLMFactory.agenerate(self.llm, messages)

            # Parse and structure the response
            # In a real implementation, you would parse the LLM response
            # and structure it according to your data model

            return {
                "title": f"{destination} {days}日游",
                "destination": destination,
                "days": days,
                "budget": budget,
                "travel_style": travel_style,
                "generated_content": response,
                "ai_generated": True
            }
        except Exception as e:
            logger.error(f"Error generating itinerary: {str(e)}")
            raise

    async def optimize_itinerary(
        self,
        itinerary: Dict[str, Any],
        feedback: str
    ) -> Dict[str, Any]:
        """
        Optimize an existing itinerary based on user feedback.

        Args:
            itinerary: Current itinerary
            feedback: User feedback for optimization

        Returns:
            Optimized itinerary
        """
        # This would implement itinerary optimization logic
        pass
