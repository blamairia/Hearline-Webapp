"""
Patient Management Module for Heartline Desktop Application

This module provides comprehensive patient management functionality including:
- CRUD operations (Create, Read, Update, Delete)
- Advanced search and filtering
- Export/Import capabilities
- Print functionality
- Bulk operations
- Advanced UI/UX features
"""

from .main_widget import PatientManagementWidget
from .dialogs.patient_dialog import PatientDialog
from .dialogs.patient_details_dialog import PatientDetailsDialog
from .widgets.patient_table import PatientTableWidget
from .widgets.patient_card import PatientCardWidget
from .utils.patient_export import PatientExporter
from .utils.patient_import import PatientImporter

__all__ = [
    'PatientManagementWidget',
    'PatientDialog',
    'PatientDetailsDialog',
    'PatientTableWidget',
    'PatientCardWidget',
    'PatientExporter',
    'PatientImporter'
]
