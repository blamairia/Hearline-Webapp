"""
Dialog Package for Patient Management

This package contains all dialog classes for patient management functionality.
"""

from .patient_dialog import PatientDialog
from .patient_details_dialog import PatientDetailsDialog

__all__ = [
    'PatientDialog',
    'PatientDetailsDialog'
]
