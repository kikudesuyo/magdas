from datetime import datetime


def convert_datetime(date: str) -> datetime:
    """Converts a string to a date object"""
    return datetime.strptime(date, "%Y-%m-%d")
