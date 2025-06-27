"""
Table widgets for displaying database data
"""

from .patients_table import PatientsTableWidget, PatientManagementWidget
from .doctors_table import DoctorsTableWidget, DoctorManagementWidget
from .appointments_table import AppointmentsTableWidget, AppointmentManagementWidget
from .visits_table import VisitsTableWidget, VisitManagementWidget
from .waiting_list_table import WaitingListTableWidget, WaitingListManagementWidget
from .prescriptions_table import PrescriptionsTableWidget
from .users_table import UsersTableWidget
from .medicaments_table import MedicamentsTableWidget
from .visit_documents_table import VisitDocumentsTableWidget
from .clinic_info_table import ClinicInfoTableWidget
from .general_settings_table import GeneralSettingsTableWidget

__all__ = [
    'PatientsTableWidget', 'PatientManagementWidget',
    'DoctorsTableWidget', 'DoctorManagementWidget',
    'AppointmentsTableWidget', 'AppointmentManagementWidget',
    'VisitsTableWidget', 'VisitManagementWidget',
    'WaitingListTableWidget', 'WaitingListManagementWidget',
    'PrescriptionsTableWidget',
    'UsersTableWidget',
    'MedicamentsTableWidget',
    'VisitDocumentsTableWidget',
    'ClinicInfoTableWidget',
    'GeneralSettingsTableWidget'
]
