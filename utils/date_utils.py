from datetime import datetime, timedelta
from dateutil.parser import parse
from typing import Optional


class DateUtils:
    @staticmethod
    def parse_date(date_str: str) -> Optional[datetime]:
        """Parse date string to datetime object"""
        try:
            return parse(date_str)
        except:
            return None

    @staticmethod
    def days_until(date: datetime) -> int:
        """Calculate days until given date"""
        return (date - datetime.now()).days

    @staticmethod
    def format_date(date: datetime, _format: str = "%B %d, %Y") -> str:
        """Format datetime object to string"""
        return date.strftime(_format)

    @staticmethod
    def get_future_date(days: int) -> datetime:
        """Get date in future by specified days"""
        return datetime.now() + timedelta(days=days)