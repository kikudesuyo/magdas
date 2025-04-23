from datetime import datetime


def to_datetime(date: str) -> datetime:
    """Converts a string to a date object"""
    return datetime.strptime(date, "%Y-%m-%d")
