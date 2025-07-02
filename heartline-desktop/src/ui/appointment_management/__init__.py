"""
Appointment Management Module

This module provides comprehensive appointment management functionality including:
- Appointment creation and editing
- Calendar views and scheduling
- Conflict detection and resolution
- Patient and doctor selection
- Reminder management
"""

try:
    from .main_widget import AppointmentManagementWidget
    from .dialogs.appointment_dialog import AppointmentDialog
    __all__ = ['AppointmentManagementWidget', 'AppointmentDialog']
except ImportError:
    # Handle import error gracefully during initial setup
    __all__ = []
