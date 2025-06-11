# app/forms/__init__.py

from .auth_forms import LoginForm, RegistrationForm, ProfileEditForm, ChangePasswordForm
from .patient_forms import PatientForm
from .visit_forms import VisitForm, PrescriptionForm, VisitDocumentForm
from .appointment_forms import AppointmentForm

__all__ = [
    'LoginForm', 'RegistrationForm', 'ProfileEditForm', 'ChangePasswordForm',
    'PatientForm', 'VisitForm', 'PrescriptionForm', 'VisitDocumentForm',
    'AppointmentForm'
]
