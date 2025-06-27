"""
Database Models for Heartline Desktop Application

This module exports all database models that exactly match the web app schema.
All models inherit from Base and follow the web app structure precisely.
"""

from .base import Base

# Import all models from complete_models (matches web app schema exactly)
from .complete_models import (
    Patient,
    Doctor,
    User,
    Appointment,
    WaitingListEntry,
    Visit,
    VisitDocument,
    Medicament,  # Unchanged structure for existing 7000+ medications
    Prescription,
    ClinicInfo,
    GeneralSettings,
    UserSession
)

# Export all models for easy importing
__all__ = [
    "Base",
    "Patient",
    "Doctor", 
    "User",
    "Appointment",
    "WaitingListEntry",
    "Visit",
    "VisitDocument",
    "Medicament",
    "Prescription",
    "ClinicInfo",
    "GeneralSettings",
    "UserSession"
]
