"""
Patient Management Widget

This widget provides comprehensive patient management functionality
including viewing, adding, editing, and searching patients.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PyQt6.QtCore import pyqtSlot

from .tables.patients_table import PatientsTableWidget

class PatientManagementWidget(QWidget):
    """Widget for patient management"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_connections()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Add patients table
        self.patients_table = PatientsTableWidget()
        layout.addWidget(self.patients_table)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.patients_table.patient_selected.connect(self.on_patient_selected)
        self.patients_table.patient_edit_requested.connect(self.on_patient_edit_requested)
    
    @pyqtSlot(int)
    def on_patient_selected(self, patient_id: int):
        """Handle patient selection"""
        print(f"Patient selected: {patient_id}")
    
    @pyqtSlot(int) 
    def on_patient_edit_requested(self, patient_id: int):
        """Handle patient edit request"""
        QMessageBox.information(self, "Edit Patient", f"Edit patient {patient_id} - Dialog will be implemented")
    
    def new_patient(self):
        """Create new patient"""
        QMessageBox.information(self, "New Patient", "New patient dialog will be implemented")
    
    def new_patient(self):
        """Create new patient"""
        pass
