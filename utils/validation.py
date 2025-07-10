import re
from typing import Optional


class Validation:
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def is_valid_doi(doi: str) -> bool:
        """Validate DOI format"""
        pattern = r'^10\.\d{4,9}/[-._;()/:A-Z0-9]+$'
        return bool(re.match(pattern, doi))

    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """Sanitize input string to prevent injection"""
        return re.sub(r'[<>]', '', input_str)

    @staticmethod
    def validate_required_field(field: str, name: str) -> Optional[str]:
        """Validate required field"""
        if not field or not field.strip():
            return f"{name} is required"
        return None