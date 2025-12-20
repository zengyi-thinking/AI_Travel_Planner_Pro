"""
Date and Time Utilities

This module provides helper functions for date and time manipulation.
"""

from datetime import datetime, timedelta
from typing import Optional
import pytz


def get_current_utc() -> datetime:
    """
    Get current UTC datetime.

    Returns:
        Current UTC datetime
    """
    return datetime.utcnow()


def format_date(date: datetime, format_str: str = "%Y-%m-%d") -> str:
    """
    Format a datetime object to string.

    Args:
        date: Datetime object
        format_str: Format string

    Returns:
        Formatted date string
    """
    return date.strftime(format_str)


def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> datetime:
    """
    Parse a date string to datetime object.

    Args:
        date_str: Date string
        format_str: Format string

    Returns:
        Parsed datetime object
    """
    return datetime.strptime(date_str, format_str)


def add_days(date: datetime, days: int) -> datetime:
    """
    Add days to a date.

    Args:
        date: Base date
        days: Number of days to add

    Returns:
        New date
    """
    return date + timedelta(days=days)


def get_date_range(start_date: datetime, end_date: datetime) -> list[datetime]:
    """
    Get a list of dates between start and end date.

    Args:
        start_date: Start date (inclusive)
        end_date: End date (inclusive)

    Returns:
        List of dates
    """
    dates = []
    current = start_date
    while current <= end_date:
        dates.append(current)
        current += timedelta(days=1)
    return dates


def is_weekend(date: datetime) -> bool:
    """
    Check if a date is weekend (Saturday or Sunday).

    Args:
        date: Date to check

    Returns:
        True if weekend, False otherwise
    """
    return date.weekday() >= 5


def get_week_number(date: datetime) -> int:
    """
    Get the ISO week number for a date.

    Args:
        date: Date to check

    Returns:
        ISO week number
    """
    return date.isocalendar()[1]
