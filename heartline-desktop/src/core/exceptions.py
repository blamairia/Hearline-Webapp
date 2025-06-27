"""
Custom exceptions for Heartline Desktop Application
"""

class HeartlineException(Exception):
    """Base exception for Heartline application"""
    pass

class DatabaseError(HeartlineException):
    """Database related errors"""
    pass

class ValidationError(HeartlineException):
    """Data validation errors"""
    pass

class BusinessLogicError(HeartlineException):
    """Business logic related errors"""
    pass

class ECGAnalysisError(HeartlineException):
    """ECG analysis related errors"""
    pass

class FileUploadError(HeartlineException):
    """File upload related errors"""
    pass

class AuthenticationError(HeartlineException):
    """Authentication related errors"""
    pass

class PermissionError(HeartlineException):
    """Permission related errors"""
    pass
