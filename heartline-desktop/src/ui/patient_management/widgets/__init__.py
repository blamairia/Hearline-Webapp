"""
Widgets Package for Patient Management

This package contains all widget classes for patient management functionality.
"""

from .patient_table import PatientTableWidget
from .patient_card import PatientCardWidget, PatientCard

__all__ = [
    'PatientTableWidget',
    'PatientCardWidget',
    'PatientCard'
]
