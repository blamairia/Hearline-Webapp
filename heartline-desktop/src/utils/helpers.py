"""
Helper utilities for Heartline Desktop Application
"""

import os
import shutil
from pathlib import Path
from typing import Optional, Tuple
import tempfile
from ..core.config import Config

class FileHelper:
    """File handling utilities"""
    
    @staticmethod
    def save_uploaded_file(file_data: bytes, filename: str, upload_type: str = "general") -> str:
        """Save uploaded file to appropriate directory"""
        # Determine upload directory based on type
        if upload_type == "ecg":
            upload_dir = Config.ECG_DIR
        elif upload_type == "documents":
            upload_dir = Config.DOCS_DIR
        else:
            upload_dir = Config.UPLOADS_DIR
        
        # Ensure directory exists
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        file_path = upload_dir / filename
        counter = 1
        while file_path.exists():
            name, ext = os.path.splitext(filename)
            file_path = upload_dir / f"{name}_{counter}{ext}"
            counter += 1
        
        # Save file
        with open(file_path, 'wb') as f:
            f.write(file_data)
        
        return str(file_path)
    
    @staticmethod
    def get_file_size_mb(file_path: str) -> float:
        """Get file size in MB"""
        return os.path.getsize(file_path) / (1024 * 1024)
    
    @staticmethod
    def is_valid_file_extension(filename: str, allowed_extensions: list) -> bool:
        """Check if file has valid extension"""
        ext = os.path.splitext(filename)[1].lower().lstrip('.')
        return ext in [e.lower() for e in allowed_extensions]

class FormatHelper:
    """Data formatting utilities"""
    
    @staticmethod
    def format_currency(amount: float, currency: str = "DZD") -> str:
        """Format currency amount"""
        return f"{amount:,.2f} {currency}"
    
    @staticmethod
    def format_percentage(value: float, decimal_places: int = 1) -> str:
        """Format percentage value"""
        return f"{value * 100:.{decimal_places}f}%"
    
    @staticmethod
    def truncate_string(text: str, max_length: int = 50) -> str:
        """Truncate string with ellipsis"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
