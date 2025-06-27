"""
Patients Table Widget for Heartline Desktop Application

This widget displays all patients in a table format with search and filtering capabilities.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QHeaderView, QLineEdit, QLabel, QMessageBox,
    QComboBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import List, Optional

from src.models.complete_models import Patient
from src.core.database import db_manager
from src.ui.styles import AppColors, AppStyles

class PatientsTableWidget(QWidget):
    """Widget for displaying and managing patients table"""
    
    # Signals
    patient_selected = pyqtSignal(int)  # Emitted when patient is selected
    patient_edit_requested = pyqtSignal(int)  # Emitted when edit is requested
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.patients: List[Patient] = []
        self.setup_ui()
        self.setup_connections()
        self.load_patients()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Apply comprehensive styling to the whole widget
        self.setStyleSheet(AppStyles.APP_STYLE)
        
        # Title
        title_label = QLabel("📋 Patients Management")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {AppColors.PRIMARY}; margin: 10px;")
        layout.addWidget(title_label)
        
        # Search and filter section
        filter_frame = QFrame()
        filter_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        filter_layout = QHBoxLayout(filter_frame)
        
        # Search box
        filter_layout.addWidget(QLabel("🔍 Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, phone, or email...")
        filter_layout.addWidget(self.search_input)
        
        # Gender filter
        filter_layout.addWidget(QLabel("Gender:"))
        self.gender_filter = QComboBox()
        self.gender_filter.addItems(["All", "Male", "Female", "Other"])
        filter_layout.addWidget(self.gender_filter)
        
        # Action buttons
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.new_patient_btn = QPushButton("➕ New Patient")
        self.edit_patient_btn = QPushButton("✏️ Edit Patient")
        self.edit_patient_btn.setEnabled(False)
        
        filter_layout.addWidget(self.refresh_btn)
        filter_layout.addWidget(self.new_patient_btn)
        filter_layout.addWidget(self.edit_patient_btn)
        
        layout.addWidget(filter_frame)
        
        # Patients table
        self.patients_table = QTableWidget()
        self.setup_table()
        layout.addWidget(self.patients_table)
        
        # Status bar
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
    
    def setup_table(self):
        """Setup the patients table with enhanced fields"""
        # Define columns including enhanced fields
        self.columns = [
            ("ID", 60),
            ("First Name", 120),
            ("Last Name", 120),
            ("Age", 60),
            ("Gender", 80),
            ("Phone", 120),
            ("Email", 180),
            ("Insurance", 140),
            ("Emergency Contact", 160),
            ("Allergies", 100),
            ("Last Visit", 120),
            ("Created", 120)
        ]
        
        self.patients_table.setColumnCount(len(self.columns))
        
        # Set headers and column widths
        headers = []
        for i, (header, width) in enumerate(self.columns):
            headers.append(header)
            self.patients_table.setColumnWidth(i, width)
        
        self.patients_table.setHorizontalHeaderLabels(headers)
        
        # Table properties
        self.patients_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.patients_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.patients_table.setAlternatingRowColors(True)
        self.patients_table.setSortingEnabled(True)
        
        # Make table headers bold
        header = self.patients_table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        
        # Apply table styling
        self.patients_table.setStyleSheet(AppStyles.get_table_style())
    
    def setup_connections(self):
        """Setup signal connections"""
        self.search_input.textChanged.connect(self.filter_patients)
        self.gender_filter.currentTextChanged.connect(self.filter_patients)
        self.refresh_btn.clicked.connect(self.load_patients)
        self.new_patient_btn.clicked.connect(self.new_patient)
        self.edit_patient_btn.clicked.connect(self.edit_selected_patient)
        self.patients_table.itemSelectionChanged.connect(self.on_selection_changed)
        self.patients_table.itemDoubleClicked.connect(self.on_double_click)
    
    def load_patients(self):
        """Load all patients from database"""
        try:
            self.status_label.setText("Loading patients...")
            
            # Create repository and fetch patients
            with db_manager.get_session() as session:
                patients = session.query(Patient).order_by(Patient.last_name, Patient.first_name).all()
                self.patients = patients
                self.populate_table(patients)
                
            self.status_label.setText(f"Loaded {len(patients)} patients")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load patients:\n{str(e)}")
            self.status_label.setText("Error loading patients")
    
    def populate_table(self, patients: List[Patient]):
        """Populate table with patient data including enhanced fields"""
        self.patients_table.setRowCount(len(patients))
        
        for row, patient in enumerate(patients):
            # ID
            self.patients_table.setItem(row, 0, QTableWidgetItem(str(patient.id)))
            
            # First Name
            self.patients_table.setItem(row, 1, QTableWidgetItem(patient.first_name))
            
            # Last Name
            self.patients_table.setItem(row, 2, QTableWidgetItem(patient.last_name))
            
            # Age
            self.patients_table.setItem(row, 3, QTableWidgetItem(str(patient.age)))
            
            # Gender
            self.patients_table.setItem(row, 4, QTableWidgetItem(patient.gender))
            
            # Phone
            phone = patient.phone or "N/A"
            self.patients_table.setItem(row, 5, QTableWidgetItem(phone))
            
            # Email
            email = patient.email or "N/A"
            self.patients_table.setItem(row, 6, QTableWidgetItem(email))
            
            # Insurance Provider (enhanced field)
            insurance = patient.insurance_provider or "N/A"
            self.patients_table.setItem(row, 7, QTableWidgetItem(insurance))
            
            # Emergency Contact (enhanced field)
            emergency_contact = patient.emergency_contact_name or "N/A"
            self.patients_table.setItem(row, 8, QTableWidgetItem(emergency_contact))
            
            # Allergies (enhanced field)
            allergies = "Yes" if patient.allergies and patient.allergies.strip() else "None"
            self.patients_table.setItem(row, 9, QTableWidgetItem(allergies))
            
            # Last Visit (placeholder)
            self.patients_table.setItem(row, 10, QTableWidgetItem("N/A"))
            
            # Created
            created = patient.created_at.strftime("%Y-%m-%d") if patient.created_at else "N/A"
            self.patients_table.setItem(row, 11, QTableWidgetItem(created))
            
            # Store patient ID in first column for reference
            self.patients_table.item(row, 0).setData(Qt.ItemDataRole.UserRole, patient.id)
    
    def filter_patients(self):
        """Filter patients based on search criteria"""
        search_text = self.search_input.text().lower()
        gender_filter = self.gender_filter.currentText()
        
        filtered_patients = []
        
        for patient in self.patients:
            # Text search
            if search_text:
                searchable_text = f"{patient.first_name} {patient.last_name} {patient.phone or ''} {patient.email or ''}".lower()
                if search_text not in searchable_text:
                    continue
            
            # Gender filter
            if gender_filter != "All" and patient.gender != gender_filter:
                continue
            
            filtered_patients.append(patient)
        
        self.populate_table(filtered_patients)
        self.status_label.setText(f"Showing {len(filtered_patients)} of {len(self.patients)} patients")
    
    def on_selection_changed(self):
        """Handle table selection change"""
        current_row = self.patients_table.currentRow()
        self.edit_patient_btn.setEnabled(current_row >= 0)
        
        if current_row >= 0:
            patient_id = self.patients_table.item(current_row, 0).data(Qt.ItemDataRole.UserRole)
            self.patient_selected.emit(patient_id)
    
    def on_double_click(self, item):
        """Handle double click on table item"""
        if item:
            self.edit_selected_patient()
    
    def new_patient(self):
        """Create new patient"""
        QMessageBox.information(self, "New Patient", "New patient dialog will be implemented")
    
    def edit_selected_patient(self):
        """Edit selected patient"""
        current_row = self.patients_table.currentRow()
        if current_row >= 0:
            patient_id = self.patients_table.item(current_row, 0).data(Qt.ItemDataRole.UserRole)
            self.patient_edit_requested.emit(patient_id)
    
    def get_selected_patient_id(self) -> Optional[int]:
        """Get ID of currently selected patient"""
        current_row = self.patients_table.currentRow()
        if current_row >= 0:
            return self.patients_table.item(current_row, 0).data(Qt.ItemDataRole.UserRole)
        return None


class PatientManagementWidget(QWidget):
    """Widget for managing patients with table view"""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the widget UI"""
        layout = QVBoxLayout()
        
        # Create table
        self.patients_table = PatientsTableWidget()
        layout.addWidget(self.patients_table)
        
        self.setLayout(layout)
    
    def refresh(self):
        """Refresh the patients data"""
        self.patients_table.load_patients()
