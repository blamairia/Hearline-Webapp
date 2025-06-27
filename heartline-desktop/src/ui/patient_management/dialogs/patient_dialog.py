"""
Patient Dialog for Creating and Editing Patients

This dialog provides a comprehensive form for creating new patients or editing existing ones.
Includes form validation, enhanced fields, and modern UI design.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QPushButton, QLineEdit, QTextEdit, QComboBox, QDateEdit, QLabel,
    QFrame, QMessageBox, QTabWidget, QWidget, QCheckBox, QSpinBox,
    QGroupBox, QScrollArea
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QIcon
from typing import Optional
from datetime import datetime, date

from src.models.complete_models import Patient
from src.core.database import db_manager
from src.ui.styles import AppColors, AppStyles


class PatientDialog(QDialog):
    """Dialog for creating or editing a patient"""
    
    patient_saved = pyqtSignal(int)  # Emitted when patient is saved
    
    def __init__(self, patient_id: Optional[int] = None, parent=None):
        super().__init__(parent)
        self.patient_id = patient_id
        self.patient = None
        self.is_editing = patient_id is not None
        
        self.setWindowTitle("Edit Patient" if self.is_editing else "New Patient")
        self.setFixedSize(800, 700)
        self.setModal(True)
        
        # Apply styles
        self.setStyleSheet(AppStyles.DIALOG_STYLE)
        
        self.setup_ui()
        self.setup_connections()
        
        if self.is_editing:
            self.load_patient()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("👤 " + ("Edit Patient" if self.is_editing else "Add New Patient"))
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {AppColors.PRIMARY}; margin: 10px;")
        layout.addWidget(title_label)
        
        # Create tabs for organized input
        self.tab_widget = QTabWidget()
        
        # Basic Information Tab
        self.basic_tab = self.create_basic_info_tab()
        self.tab_widget.addTab(self.basic_tab, "📋 Basic Info")
        
        # Contact Information Tab
        self.contact_tab = self.create_contact_info_tab()
        self.tab_widget.addTab(self.contact_tab, "📞 Contact")
        
        # Medical Information Tab
        self.medical_tab = self.create_medical_info_tab()
        self.tab_widget.addTab(self.medical_tab, "🏥 Medical")
        
        # Emergency & Insurance Tab
        self.emergency_tab = self.create_emergency_info_tab()
        self.tab_widget.addTab(self.emergency_tab, "🚨 Emergency & Insurance")
        
        layout.addWidget(self.tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.cancel_btn = QPushButton("❌ Cancel")
        self.save_btn = QPushButton("💾 Save Patient")
        self.save_and_new_btn = QPushButton("💾➕ Save & Add New")
        
        if self.is_editing:
            self.delete_btn = QPushButton("🗑️ Delete")
            self.delete_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; }")
            button_layout.addWidget(self.delete_btn)
        
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.save_btn)
        
        if not self.is_editing:
            button_layout.addWidget(self.save_and_new_btn)
        
        layout.addLayout(button_layout)
    
    def create_basic_info_tab(self) -> QWidget:
        """Create the basic information tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # Personal Information Group
        personal_group = QGroupBox("Personal Information")
        personal_layout = QFormLayout(personal_group)
        
        self.first_name_edit = QLineEdit()
        self.first_name_edit.setPlaceholderText("Enter first name")
        personal_layout.addRow("*First Name:", self.first_name_edit)
        
        self.last_name_edit = QLineEdit()
        self.last_name_edit.setPlaceholderText("Enter last name")
        personal_layout.addRow("*Last Name:", self.last_name_edit)
        
        self.date_of_birth_edit = QDateEdit()
        self.date_of_birth_edit.setDate(QDate.currentDate().addYears(-30))
        self.date_of_birth_edit.setCalendarPopup(True)
        personal_layout.addRow("*Date of Birth:", self.date_of_birth_edit)
        
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female", "Other"])
        personal_layout.addRow("*Gender:", self.gender_combo)
        
        self.blood_type_combo = QComboBox()
        self.blood_type_combo.addItems(["Unknown", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        personal_layout.addRow("Blood Type:", self.blood_type_combo)
        
        layout.addRow(personal_group)
        
        # Identification Group
        id_group = QGroupBox("Identification")
        id_layout = QFormLayout(id_group)
        
        self.ssn_edit = QLineEdit()
        self.ssn_edit.setPlaceholderText("XXX-XX-XXXX")
        id_layout.addRow("SSN:", self.ssn_edit)
        
        self.id_number_edit = QLineEdit()
        self.id_number_edit.setPlaceholderText("Government ID number")
        id_layout.addRow("ID Number:", self.id_number_edit)
        
        layout.addRow(id_group)
        
        return widget
    
    def create_contact_info_tab(self) -> QWidget:
        """Create the contact information tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # Contact Information Group
        contact_group = QGroupBox("Contact Information")
        contact_layout = QFormLayout(contact_group)
        
        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("(XXX) XXX-XXXX")
        contact_layout.addRow("Phone:", self.phone_edit)
        
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("patient@email.com")
        contact_layout.addRow("Email:", self.email_edit)
        
        layout.addRow(contact_group)
        
        # Address Group
        address_group = QGroupBox("Address")
        address_layout = QFormLayout(address_group)
        
        self.address_edit = QLineEdit()
        self.address_edit.setPlaceholderText("Street address")
        address_layout.addRow("Address:", self.address_edit)
        
        self.city_edit = QLineEdit()
        self.city_edit.setPlaceholderText("City")
        address_layout.addRow("City:", self.city_edit)
        
        self.state_edit = QLineEdit()
        self.state_edit.setPlaceholderText("State")
        address_layout.addRow("State:", self.state_edit)
        
        self.zip_code_edit = QLineEdit()
        self.zip_code_edit.setPlaceholderText("ZIP Code")
        address_layout.addRow("ZIP Code:", self.zip_code_edit)
        
        self.country_edit = QLineEdit()
        self.country_edit.setPlaceholderText("Country")
        self.country_edit.setText("United States")
        address_layout.addRow("Country:", self.country_edit)
        
        layout.addRow(address_group)
        
        return widget
    
    def create_medical_info_tab(self) -> QWidget:
        """Create the medical information tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Create scroll area for medical info
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QFormLayout(scroll_widget)
        
        # Medical History Group
        medical_group = QGroupBox("Medical History")
        medical_layout = QFormLayout(medical_group)
        
        self.allergies_edit = QTextEdit()
        self.allergies_edit.setPlaceholderText("List any known allergies...")
        self.allergies_edit.setMaximumHeight(80)
        medical_layout.addRow("Allergies:", self.allergies_edit)
        
        self.chronic_conditions_edit = QTextEdit()
        self.chronic_conditions_edit.setPlaceholderText("List chronic conditions...")
        self.chronic_conditions_edit.setMaximumHeight(80)
        medical_layout.addRow("Chronic Conditions:", self.chronic_conditions_edit)
        
        self.current_medications_edit = QTextEdit()
        self.current_medications_edit.setPlaceholderText("List current medications...")
        self.current_medications_edit.setMaximumHeight(80)
        medical_layout.addRow("Current Medications:", self.current_medications_edit)
        
        self.family_history_edit = QTextEdit()
        self.family_history_edit.setPlaceholderText("Family medical history...")
        self.family_history_edit.setMaximumHeight(80)
        medical_layout.addRow("Family History:", self.family_history_edit)
        
        scroll_layout.addRow(medical_group)
        
        # Physical Information Group
        physical_group = QGroupBox("Physical Information")
        physical_layout = QFormLayout(physical_group)
        
        self.height_edit = QSpinBox()
        self.height_edit.setRange(50, 300)  # cm
        self.height_edit.setSuffix(" cm")
        self.height_edit.setValue(170)
        physical_layout.addRow("Height:", self.height_edit)
        
        self.weight_edit = QSpinBox()
        self.weight_edit.setRange(1, 500)  # kg
        self.weight_edit.setSuffix(" kg")
        self.weight_edit.setValue(70)
        physical_layout.addRow("Weight:", self.weight_edit)
        
        scroll_layout.addRow(physical_group)
        
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        return widget
    
    def create_emergency_info_tab(self) -> QWidget:
        """Create the emergency and insurance information tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # Emergency Contact Group
        emergency_group = QGroupBox("Emergency Contact")
        emergency_layout = QFormLayout(emergency_group)
        
        self.emergency_name_edit = QLineEdit()
        self.emergency_name_edit.setPlaceholderText("Contact name")
        emergency_layout.addRow("Name:", self.emergency_name_edit)
        
        self.emergency_relationship_edit = QLineEdit()
        self.emergency_relationship_edit.setPlaceholderText("Relationship")
        emergency_layout.addRow("Relationship:", self.emergency_relationship_edit)
        
        self.emergency_phone_edit = QLineEdit()
        self.emergency_phone_edit.setPlaceholderText("(XXX) XXX-XXXX")
        emergency_layout.addRow("Phone:", self.emergency_phone_edit)
        
        layout.addRow(emergency_group)
        
        # Insurance Information Group
        insurance_group = QGroupBox("Insurance Information")
        insurance_layout = QFormLayout(insurance_group)
        
        self.insurance_provider_edit = QLineEdit()
        self.insurance_provider_edit.setPlaceholderText("Insurance company name")
        insurance_layout.addRow("Provider:", self.insurance_provider_edit)
        
        self.insurance_number_edit = QLineEdit()
        self.insurance_number_edit.setPlaceholderText("Policy number")
        insurance_layout.addRow("Policy Number:", self.insurance_number_edit)
        
        self.insurance_group_edit = QLineEdit()
        self.insurance_group_edit.setPlaceholderText("Group number")
        insurance_layout.addRow("Group Number:", self.insurance_group_edit)
        
        layout.addRow(insurance_group)
        
        # Preferences Group
        prefs_group = QGroupBox("Preferences")
        prefs_layout = QFormLayout(prefs_group)
        
        self.preferred_language_combo = QComboBox()
        self.preferred_language_combo.addItems(["English", "Spanish", "French", "Other"])
        prefs_layout.addRow("Preferred Language:", self.preferred_language_combo)
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Additional notes...")
        self.notes_edit.setMaximumHeight(80)
        prefs_layout.addRow("Notes:", self.notes_edit)
        
        layout.addRow(prefs_group)
        
        return widget
    
    def setup_connections(self):
        """Setup signal connections"""
        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self.save_patient)
        
        if not self.is_editing:
            self.save_and_new_btn.clicked.connect(self.save_and_new)
        
        if self.is_editing:
            self.delete_btn.clicked.connect(self.delete_patient)
    
    def load_patient(self):
        """Load patient data for editing"""
        try:
            with db_manager.get_session() as session:
                patient = session.query(Patient).filter(Patient.id == self.patient_id).first()
                if not patient:
                    QMessageBox.critical(self, "Error", "Patient not found!")
                    self.reject()
                    return
                
                # Extract data before session closes
                self.patient = patient
                
                # Populate form fields
                self.first_name_edit.setText(patient.first_name or "")
                self.last_name_edit.setText(patient.last_name or "")
                
                if patient.date_of_birth:
                    self.date_of_birth_edit.setDate(QDate(patient.date_of_birth))
                
                if patient.gender:
                    index = self.gender_combo.findText(patient.gender)
                    if index >= 0:
                        self.gender_combo.setCurrentIndex(index)
                
                self.phone_edit.setText(patient.phone or "")
                self.email_edit.setText(patient.email or "")
                self.address_edit.setText(patient.address or "")
                self.city_edit.setText(patient.city or "")
                self.state_edit.setText(patient.state or "")
                self.zip_code_edit.setText(patient.zip_code or "")
                self.country_edit.setText(patient.country or "")
                
                # Medical information
                self.allergies_edit.setPlainText(patient.allergies or "")
                self.chronic_conditions_edit.setPlainText(patient.chronic_conditions or "")
                self.current_medications_edit.setPlainText(patient.current_medications or "")
                self.family_history_edit.setPlainText(patient.family_history or "")
                
                if patient.height:
                    self.height_edit.setValue(patient.height)
                if patient.weight:
                    self.weight_edit.setValue(patient.weight)
                
                if patient.blood_type:
                    index = self.blood_type_combo.findText(patient.blood_type)
                    if index >= 0:
                        self.blood_type_combo.setCurrentIndex(index)
                
                # Emergency and insurance
                self.emergency_name_edit.setText(patient.emergency_contact_name or "")
                self.emergency_relationship_edit.setText(patient.emergency_contact_relationship or "")
                self.emergency_phone_edit.setText(patient.emergency_contact_phone or "")
                
                self.insurance_provider_edit.setText(patient.insurance_provider or "")
                self.insurance_number_edit.setText(patient.insurance_number or "")
                self.insurance_group_edit.setText(patient.insurance_group or "")
                
                if patient.preferred_language:
                    index = self.preferred_language_combo.findText(patient.preferred_language)
                    if index >= 0:
                        self.preferred_language_combo.setCurrentIndex(index)
                
                self.notes_edit.setPlainText(patient.notes or "")
                self.ssn_edit.setText(patient.ssn or "")
                self.id_number_edit.setText(patient.id_number or "")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load patient:\n{str(e)}")
            self.reject()
    
    def validate_form(self) -> bool:
        """Validate form inputs"""
        if not self.first_name_edit.text().strip():
            QMessageBox.warning(self, "Validation Error", "First name is required!")
            self.first_name_edit.setFocus()
            return False
        
        if not self.last_name_edit.text().strip():
            QMessageBox.warning(self, "Validation Error", "Last name is required!")
            self.last_name_edit.setFocus()
            return False
        
        # Validate email format if provided
        email = self.email_edit.text().strip()
        if email and "@" not in email:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid email address!")
            self.email_edit.setFocus()
            return False
        
        return True
    
    def calculate_age(self, birth_date: date) -> int:
        """Calculate age from birth date"""
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    def save_patient(self):
        """Save patient data"""
        if not self.validate_form():
            return
        
        try:
            with db_manager.get_session() as session:
                if self.is_editing:
                    patient = session.query(Patient).filter(Patient.id == self.patient_id).first()
                    if not patient:
                        QMessageBox.critical(self, "Error", "Patient not found!")
                        return
                else:
                    patient = Patient()
                    session.add(patient)
                
                # Update patient data
                patient.first_name = self.first_name_edit.text().strip()
                patient.last_name = self.last_name_edit.text().strip()
                patient.date_of_birth = self.date_of_birth_edit.date().toPyDate()
                # Note: age is calculated automatically as a property from date_of_birth
                patient.gender = self.gender_combo.currentText()
                patient.phone = self.phone_edit.text().strip() or None
                patient.email = self.email_edit.text().strip() or None
                patient.address = self.address_edit.text().strip() or None
                patient.city = self.city_edit.text().strip() or None
                patient.state = self.state_edit.text().strip() or None
                patient.zip_code = self.zip_code_edit.text().strip() or None
                patient.country = self.country_edit.text().strip() or None
                
                # Medical information
                patient.allergies = self.allergies_edit.toPlainText().strip() or None
                patient.chronic_conditions = self.chronic_conditions_edit.toPlainText().strip() or None
                patient.current_medications = self.current_medications_edit.toPlainText().strip() or None
                patient.family_history = self.family_history_edit.toPlainText().strip() or None
                patient.height = self.height_edit.value()
                patient.weight = self.weight_edit.value()
                patient.blood_type = self.blood_type_combo.currentText() if self.blood_type_combo.currentText() != "Unknown" else None
                
                # Emergency and insurance
                patient.emergency_contact_name = self.emergency_name_edit.text().strip() or None
                patient.emergency_contact_relationship = self.emergency_relationship_edit.text().strip() or None
                patient.emergency_contact_phone = self.emergency_phone_edit.text().strip() or None
                patient.insurance_provider = self.insurance_provider_edit.text().strip() or None
                patient.insurance_number = self.insurance_number_edit.text().strip() or None
                patient.insurance_group = self.insurance_group_edit.text().strip() or None
                patient.preferred_language = self.preferred_language_combo.currentText()
                patient.notes = self.notes_edit.toPlainText().strip() or None
                patient.ssn = self.ssn_edit.text().strip() or None
                patient.id_number = self.id_number_edit.text().strip() or None
                
                if not self.is_editing:
                    patient.created_at = datetime.now()
                
                session.commit()
                
                # Get the patient ID for the signal
                patient_id = patient.id
                
            self.patient_saved.emit(patient_id)
            
            action = "updated" if self.is_editing else "created"
            QMessageBox.information(self, "Success", f"Patient {action} successfully!")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save patient:\n{str(e)}")
    
    def save_and_new(self):
        """Save current patient and open new dialog"""
        if not self.validate_form():
            return
        
        self.save_patient()
        
        # Clear form for new patient
        self.clear_form()
    
    def clear_form(self):
        """Clear all form fields"""
        self.first_name_edit.clear()
        self.last_name_edit.clear()
        self.date_of_birth_edit.setDate(QDate.currentDate().addYears(-30))
        self.gender_combo.setCurrentIndex(0)
        self.phone_edit.clear()
        self.email_edit.clear()
        self.address_edit.clear()
        self.city_edit.clear()
        self.state_edit.clear()
        self.zip_code_edit.clear()
        self.country_edit.setText("United States")
        self.allergies_edit.clear()
        self.chronic_conditions_edit.clear()
        self.current_medications_edit.clear()
        self.family_history_edit.clear()
        self.height_edit.setValue(170)
        self.weight_edit.setValue(70)
        self.blood_type_combo.setCurrentIndex(0)
        self.emergency_name_edit.clear()
        self.emergency_relationship_edit.clear()
        self.emergency_phone_edit.clear()
        self.insurance_provider_edit.clear()
        self.insurance_number_edit.clear()
        self.insurance_group_edit.clear()
        self.preferred_language_combo.setCurrentIndex(0)
        self.notes_edit.clear()
        self.ssn_edit.clear()
        self.id_number_edit.clear()
        
        # Focus on first field
        self.first_name_edit.setFocus()
    
    def delete_patient(self):
        """Delete the current patient"""
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete patient {self.patient.first_name} {self.patient.last_name}?\n\n"
            "This action cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                with db_manager.get_session() as session:
                    patient = session.query(Patient).filter(Patient.id == self.patient_id).first()
                    if patient:
                        session.delete(patient)
                        session.commit()
                
                QMessageBox.information(self, "Success", "Patient deleted successfully!")
                self.patient_saved.emit(self.patient_id)  # Signal refresh
                self.accept()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete patient:\n{str(e)}")
