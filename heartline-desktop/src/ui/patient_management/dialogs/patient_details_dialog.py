"""
Patient Details Dialog for Viewing Complete Patient Information

This dialog provides a comprehensive, read-only view of patient information
with professional medical record formatting.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QTabWidget, QWidget, QScrollArea, QFrame,
    QGroupBox, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
from typing import Optional
from datetime import date

from src.models.complete_models import Patient, Visit, Prescription
from src.core.database import db_manager
from src.ui.styles import AppColors, AppStyles


class PatientDetailsDialog(QDialog):
    """Dialog for viewing comprehensive patient details"""
    
    edit_requested = pyqtSignal(int)  # Emitted when edit is requested
    
    def __init__(self, patient_id: int, parent=None):
        super().__init__(parent)
        self.patient_id = patient_id
        self.patient = None
        
        self.setWindowTitle("Patient Details")
        self.setFixedSize(900, 700)
        self.setModal(True)
        
        # Apply styles
        self.setStyleSheet(AppStyles.DIALOG_STYLE)
        
        self.setup_ui()
        self.load_patient_data()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Header with patient basic info
        self.header_frame = self.create_header()
        layout.addWidget(self.header_frame)
        
        # Tabs for detailed information
        self.tab_widget = QTabWidget()
        
        # Personal Information Tab
        self.personal_tab = self.create_personal_tab()
        self.tab_widget.addTab(self.personal_tab, "👤 Personal")
        
        # Medical Information Tab
        self.medical_tab = self.create_medical_tab()
        self.tab_widget.addTab(self.medical_tab, "🏥 Medical")
        
        # Visit History Tab
        self.visits_tab = self.create_visits_tab()
        self.tab_widget.addTab(self.visits_tab, "📅 Visits")
        
        # Prescriptions Tab
        self.prescriptions_tab = self.create_prescriptions_tab()
        self.tab_widget.addTab(self.prescriptions_tab, "💊 Prescriptions")
        
        layout.addWidget(self.tab_widget)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.print_btn = QPushButton("🖨️ Print")
        self.export_btn = QPushButton("📄 Export")
        self.edit_btn = QPushButton("✏️ Edit Patient")
        self.close_btn = QPushButton("❌ Close")
        
        button_layout.addWidget(self.print_btn)
        button_layout.addWidget(self.export_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
        
        # Connect signals
        self.edit_btn.clicked.connect(self.edit_patient)
        self.close_btn.clicked.connect(self.accept)
        self.print_btn.clicked.connect(self.print_patient)
        self.export_btn.clicked.connect(self.export_patient)
    
    def create_header(self) -> QFrame:
        """Create the header with patient summary"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {AppColors.BACKGROUND};
                border: 2px solid {AppColors.PRIMARY};
                border-radius: 10px;
                padding: 10px;
            }}
        """)
        
        layout = QHBoxLayout(frame)
        
        # Patient avatar placeholder
        avatar_label = QLabel()
        avatar_label.setFixedSize(80, 80)
        avatar_label.setStyleSheet(f"""
            QLabel {{
                background-color: {AppColors.PRIMARY};
                border-radius: 40px;
                color: white;
                font-size: 24px;
                font-weight: bold;
            }}
        """)
        avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar_label.setText("👤")
        layout.addWidget(avatar_label)
        
        # Patient info
        info_layout = QVBoxLayout()
        
        self.name_label = QLabel()
        self.name_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.name_label.setStyleSheet(f"color: {AppColors.PRIMARY};")
        info_layout.addWidget(self.name_label)
        
        self.details_label = QLabel()
        self.details_label.setFont(QFont("Segoe UI", 11))
        info_layout.addWidget(self.details_label)
        
        self.contact_label = QLabel()
        self.contact_label.setFont(QFont("Segoe UI", 10))
        self.contact_label.setStyleSheet(f"color: {AppColors.TEXT_SECONDARY};")
        info_layout.addWidget(self.contact_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        return frame
    
    def create_personal_tab(self) -> QWidget:
        """Create personal information tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Basic Information Group
        basic_group = QGroupBox("Basic Information")
        basic_layout = QGridLayout(basic_group)
        
        self.first_name_label = QLabel()
        self.last_name_label = QLabel()
        self.dob_label = QLabel()
        self.age_label = QLabel()
        self.gender_label = QLabel()
        self.blood_type_label = QLabel()
        
        basic_layout.addWidget(QLabel("First Name:"), 0, 0)
        basic_layout.addWidget(self.first_name_label, 0, 1)
        basic_layout.addWidget(QLabel("Last Name:"), 0, 2)
        basic_layout.addWidget(self.last_name_label, 0, 3)
        basic_layout.addWidget(QLabel("Date of Birth:"), 1, 0)
        basic_layout.addWidget(self.dob_label, 1, 1)
        basic_layout.addWidget(QLabel("Age:"), 1, 2)
        basic_layout.addWidget(self.age_label, 1, 3)
        basic_layout.addWidget(QLabel("Gender:"), 2, 0)
        basic_layout.addWidget(self.gender_label, 2, 1)
        basic_layout.addWidget(QLabel("Blood Type:"), 2, 2)
        basic_layout.addWidget(self.blood_type_label, 2, 3)
        
        scroll_layout.addWidget(basic_group)
        
        # Contact Information Group
        contact_group = QGroupBox("Contact Information")
        contact_layout = QGridLayout(contact_group)
        
        self.phone_label = QLabel()
        self.email_label = QLabel()
        self.address_label = QLabel()
        
        contact_layout.addWidget(QLabel("Phone:"), 0, 0)
        contact_layout.addWidget(self.phone_label, 0, 1)
        contact_layout.addWidget(QLabel("Email:"), 0, 2)
        contact_layout.addWidget(self.email_label, 0, 3)
        contact_layout.addWidget(QLabel("Address:"), 1, 0)
        contact_layout.addWidget(self.address_label, 1, 1, 1, 3)
        
        scroll_layout.addWidget(contact_group)
        
        # Emergency Contact Group
        emergency_group = QGroupBox("Emergency Contact")
        emergency_layout = QGridLayout(emergency_group)
        
        self.emergency_name_label = QLabel()
        self.emergency_relationship_label = QLabel()
        self.emergency_phone_label = QLabel()
        
        emergency_layout.addWidget(QLabel("Name:"), 0, 0)
        emergency_layout.addWidget(self.emergency_name_label, 0, 1)
        emergency_layout.addWidget(QLabel("Relationship:"), 0, 2)
        emergency_layout.addWidget(self.emergency_relationship_label, 0, 3)
        emergency_layout.addWidget(QLabel("Phone:"), 1, 0)
        emergency_layout.addWidget(self.emergency_phone_label, 1, 1)
        
        scroll_layout.addWidget(emergency_group)
        
        # Insurance Information Group
        insurance_group = QGroupBox("Insurance Information")
        insurance_layout = QGridLayout(insurance_group)
        
        self.insurance_provider_label = QLabel()
        self.insurance_number_label = QLabel()
        self.insurance_group_label = QLabel()
        
        insurance_layout.addWidget(QLabel("Provider:"), 0, 0)
        insurance_layout.addWidget(self.insurance_provider_label, 0, 1)
        insurance_layout.addWidget(QLabel("Policy Number:"), 0, 2)
        insurance_layout.addWidget(self.insurance_number_label, 0, 3)
        insurance_layout.addWidget(QLabel("Group Number:"), 1, 0)
        insurance_layout.addWidget(self.insurance_group_label, 1, 1)
        
        scroll_layout.addWidget(insurance_group)
        
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        return widget
    
    def create_medical_tab(self) -> QWidget:
        """Create medical information tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Physical Information Group
        physical_group = QGroupBox("Physical Information")
        physical_layout = QGridLayout(physical_group)
        
        self.height_label = QLabel()
        self.weight_label = QLabel()
        self.bmi_label = QLabel()
        
        physical_layout.addWidget(QLabel("Height:"), 0, 0)
        physical_layout.addWidget(self.height_label, 0, 1)
        physical_layout.addWidget(QLabel("Weight:"), 0, 2)
        physical_layout.addWidget(self.weight_label, 0, 3)
        physical_layout.addWidget(QLabel("BMI:"), 1, 0)
        physical_layout.addWidget(self.bmi_label, 1, 1)
        
        scroll_layout.addWidget(physical_group)
        
        # Medical History Groups
        allergies_group = QGroupBox("Allergies")
        allergies_layout = QVBoxLayout(allergies_group)
        self.allergies_text = QTextEdit()
        self.allergies_text.setReadOnly(True)
        self.allergies_text.setMaximumHeight(100)
        allergies_layout.addWidget(self.allergies_text)
        scroll_layout.addWidget(allergies_group)
        
        conditions_group = QGroupBox("Chronic Conditions")
        conditions_layout = QVBoxLayout(conditions_group)
        self.conditions_text = QTextEdit()
        self.conditions_text.setReadOnly(True)
        self.conditions_text.setMaximumHeight(100)
        conditions_layout.addWidget(self.conditions_text)
        scroll_layout.addWidget(conditions_group)
        
        medications_group = QGroupBox("Current Medications")
        medications_layout = QVBoxLayout(medications_group)
        self.medications_text = QTextEdit()
        self.medications_text.setReadOnly(True)
        self.medications_text.setMaximumHeight(100)
        medications_layout.addWidget(self.medications_text)
        scroll_layout.addWidget(medications_group)
        
        family_group = QGroupBox("Family History")
        family_layout = QVBoxLayout(family_group)
        self.family_text = QTextEdit()
        self.family_text.setReadOnly(True)
        self.family_text.setMaximumHeight(100)
        family_layout.addWidget(self.family_text)
        scroll_layout.addWidget(family_group)
        
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        return widget
    
    def create_visits_tab(self) -> QWidget:
        """Create visits history tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.visits_label = QLabel("Visit history will be displayed here")
        self.visits_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.visits_label)
        
        return widget
    
    def create_prescriptions_tab(self) -> QWidget:
        """Create prescriptions tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.prescriptions_label = QLabel("Prescription history will be displayed here")
        self.prescriptions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.prescriptions_label)
        
        return widget
    
    def load_patient_data(self):
        """Load patient data from database"""
        try:
            with db_manager.get_session() as session:
                patient = session.query(Patient).filter(Patient.id == self.patient_id).first()
                if not patient:
                    QMessageBox.critical(self, "Error", "Patient not found!")
                    self.reject()
                    return
                
                # Extract all data before session closes
                self.patient = patient
                
                # Update header
                full_name = f"{patient.first_name} {patient.last_name}"
                self.name_label.setText(full_name)
                
                age_text = f"Age: {patient.age}" if patient.age else "Age: Unknown"
                gender_text = f"Gender: {patient.gender}" if patient.gender else ""
                self.details_label.setText(f"{age_text} • {gender_text}")
                
                contact_parts = []
                if patient.phone:
                    contact_parts.append(f"📞 {patient.phone}")
                if patient.email:
                    contact_parts.append(f"📧 {patient.email}")
                self.contact_label.setText(" • ".join(contact_parts))
                
                # Update personal tab
                self.first_name_label.setText(patient.first_name or "N/A")
                self.last_name_label.setText(patient.last_name or "N/A")
                self.dob_label.setText(patient.date_of_birth.strftime("%B %d, %Y") if patient.date_of_birth else "N/A")
                self.age_label.setText(str(patient.age) if patient.age else "N/A")
                self.gender_label.setText(patient.gender or "N/A")
                self.blood_type_label.setText(patient.blood_type or "N/A")
                
                self.phone_label.setText(patient.phone or "N/A")
                self.email_label.setText(patient.email or "N/A")
                
                # Construct full address
                address_parts = []
                if patient.address:
                    address_parts.append(patient.address)
                if patient.city:
                    address_parts.append(patient.city)
                if patient.state:
                    address_parts.append(patient.state)
                if patient.zip_code:
                    address_parts.append(patient.zip_code)
                if patient.country:
                    address_parts.append(patient.country)
                
                self.address_label.setText(", ".join(address_parts) if address_parts else "N/A")
                
                # Emergency contact
                self.emergency_name_label.setText(patient.emergency_contact_name or "N/A")
                self.emergency_relationship_label.setText(patient.emergency_contact_relationship or "N/A")
                self.emergency_phone_label.setText(patient.emergency_contact_phone or "N/A")
                
                # Insurance
                self.insurance_provider_label.setText(patient.insurance_provider or "N/A")
                self.insurance_number_label.setText(patient.insurance_number or "N/A")
                self.insurance_group_label.setText(patient.insurance_group or "N/A")
                
                # Medical information
                if patient.height and patient.weight:
                    self.height_label.setText(f"{patient.height} cm")
                    self.weight_label.setText(f"{patient.weight} kg")
                    # Calculate BMI
                    height_m = patient.height / 100
                    bmi = patient.weight / (height_m * height_m)
                    self.bmi_label.setText(f"{bmi:.1f}")
                else:
                    self.height_label.setText("N/A")
                    self.weight_label.setText("N/A")
                    self.bmi_label.setText("N/A")
                
                self.allergies_text.setPlainText(patient.allergies or "No known allergies")
                self.conditions_text.setPlainText(patient.chronic_conditions or "No chronic conditions recorded")
                self.medications_text.setPlainText(patient.current_medications or "No current medications")
                self.family_text.setPlainText(patient.family_history or "No family history recorded")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load patient data:\n{str(e)}")
            self.reject()
    
    def edit_patient(self):
        """Request to edit the patient"""
        self.edit_requested.emit(self.patient_id)
        self.accept()
    
    def print_patient(self):
        """Print patient information"""
        QMessageBox.information(self, "Print", "Print functionality will be implemented")
    
    def export_patient(self):
        """Export patient information"""
        QMessageBox.information(self, "Export", "Export functionality will be implemented")
