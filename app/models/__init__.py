# app/models/__init__.py

from app.extensions import db, bcrypt
from .patient import Patient
from .doctor import Doctor
from .appointment import Appointment
from .visit import Visit, VisitDocument
from .prescription import Prescription, Medicament
from .user import User, UserSession
from .settings import ClinicInfo, GeneralSettings
from .waiting_list import WaitingListEntry

__all__ = [
    'db', 'bcrypt',
    'Patient', 'Doctor', 'Appointment', 'Visit', 'VisitDocument',
    'Prescription', 'Medicament', 'User', 'UserSession',
    'ClinicInfo', 'GeneralSettings', 'WaitingListEntry'
]
