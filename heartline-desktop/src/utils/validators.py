"""
Data validation utilities for Heartline Desktop Application
"""

import re
from datetime import datetime, date
from typing import Any, Dict, List, Optional
from ..core.exceptions import ValidationError

class Validators:
    """Collection of data validation functions"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        # Remove spaces and dashes
        clean_phone = re.sub(r'[\s-]', '', phone)
        # Check if it contains only digits and optional + at start
        pattern = r'^\+?[0-9]{8,15}$'
        return re.match(pattern, clean_phone) is not None
    
    @staticmethod
    def validate_date_string(date_string: str) -> bool:
        """Validate date string format (YYYY-MM-DD)"""
        try:
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_required_fields(data: Dict, required_fields: List[str]):
        """Validate that all required fields are present and not empty"""
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValidationError(f"Required field missing or empty: {field}")
    
    @staticmethod
    def validate_string_length(value: str, min_length: int = 0, max_length: int = 255) -> bool:
        """Validate string length"""
        return min_length <= len(value) <= max_length
    
    @staticmethod
    def validate_numeric_range(value: float, min_value: float = None, max_value: float = None) -> bool:
        """Validate numeric value range"""
        if min_value is not None and value < min_value:
            return False
        if max_value is not None and value > max_value:
            return False
        return True
