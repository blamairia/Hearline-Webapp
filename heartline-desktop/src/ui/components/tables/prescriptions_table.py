"""
Prescriptions Table Widget for Heartline Desktop Application

This widget displays all prescriptions in a table format with search and filtering capabilities.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QHeaderView, QLineEdit, QLabel, QMessageBox,
    QComboBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import List, Optional

from src.models.complete_models import Prescription
from src.core.database import db_manager
from src.ui.styles import AppColors, AppStyles

class PrescriptionsTableWidget(QWidget):
    """Widget for displaying and managing prescriptions table"""
    
    # Signals
    prescription_selected = pyqtSignal(int)  # Emitted when prescription is selected
    prescription_edit_requested = pyqtSignal(int)  # Emitted when edit is requested
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.prescriptions: List[Prescription] = []
        self.setup_ui()
        self.setup_connections()
        self.load_prescriptions()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Apply comprehensive styling to the whole widget
        self.setStyleSheet(AppStyles.APP_STYLE)
        
        # Title
        title_label = QLabel("💊 Prescriptions Management")
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
        self.search_input.setPlaceholderText("Search by medication name or patient...")
        filter_layout.addWidget(self.search_input)
        
        # Filter by visit
        filter_layout.addWidget(QLabel("Visit:"))
        self.visit_filter = QComboBox()
        self.visit_filter.addItem("All Visits")
        filter_layout.addWidget(self.visit_filter)
        
        # Action buttons
        filter_layout.addStretch()
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.new_prescription_btn = QPushButton("➕ New Prescription")
        self.edit_prescription_btn = QPushButton("✏️ Edit")
        self.delete_prescription_btn = QPushButton("🗑️ Delete")
        
        self.refresh_btn.setObjectName("primary-button")
        self.new_prescription_btn.setObjectName("success-button")
        self.edit_prescription_btn.setObjectName("primary-button")
        self.delete_prescription_btn.setObjectName("danger-button")
        
        filter_layout.addWidget(self.refresh_btn)
        filter_layout.addWidget(self.new_prescription_btn)
        filter_layout.addWidget(self.edit_prescription_btn)
        filter_layout.addWidget(self.delete_prescription_btn)
        
        layout.addWidget(filter_frame)
        
        # Prescriptions table
        self.setup_table()
        layout.addWidget(self.prescriptions_table)
        
        # Status bar
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #666; padding: 5px;")
        layout.addWidget(self.status_label)
    
    def setup_table(self):
        """Setup the prescriptions table"""
        # Define columns
        self.columns = [
            ("ID", 60),
            ("Visit ID", 80),
            ("Patient", 150),
            ("Doctor", 150),
            ("Medication", 180),
            ("Dosage Instructions", 200),
            ("Quantity", 80),
            ("Created", 120)
        ]
        
        self.prescriptions_table = QTableWidget()
        self.prescriptions_table.setColumnCount(len(self.columns))
        
        # Set headers and column widths
        headers = []
        for i, (header, width) in enumerate(self.columns):
            headers.append(header)
            self.prescriptions_table.setColumnWidth(i, width)
        
        self.prescriptions_table.setHorizontalHeaderLabels(headers)
        
        # Table properties
        self.prescriptions_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.prescriptions_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.prescriptions_table.setAlternatingRowColors(True)
        self.prescriptions_table.setSortingEnabled(True)
        
        # Apply table styling
        self.prescriptions_table.setStyleSheet(AppStyles.get_table_style())
        # Make table headers bold
        header = self.prescriptions_table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.search_input.textChanged.connect(self.filter_prescriptions)
        self.visit_filter.currentTextChanged.connect(self.filter_prescriptions)
        self.refresh_btn.clicked.connect(self.load_prescriptions)
        self.new_prescription_btn.clicked.connect(self.new_prescription)
        self.edit_prescription_btn.clicked.connect(self.edit_selected_prescription)
        self.delete_prescription_btn.clicked.connect(self.delete_selected_prescription)
        self.prescriptions_table.itemSelectionChanged.connect(self.on_selection_changed)
        self.prescriptions_table.itemDoubleClicked.connect(self.on_double_click)
    
    def load_prescriptions(self):
        """Load all prescriptions from database"""
        try:
            self.status_label.setText("Loading prescriptions...")
            
            with db_manager.get_session() as session:
                prescriptions = session.query(Prescription).join(Prescription.visit).join(Prescription.medicament).order_by(Prescription.created_at.desc()).all()
                self.prescriptions = prescriptions
                self.populate_table(prescriptions)
                
            self.status_label.setText(f"Loaded {len(prescriptions)} prescriptions")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load prescriptions:\n{str(e)}")
            self.status_label.setText("Error loading prescriptions")
    
    def populate_table(self, prescriptions: List[Prescription]):
        """Populate table with prescription data"""
        self.prescriptions_table.setRowCount(len(prescriptions))
        
        for row, prescription in enumerate(prescriptions):
            # ID
            self.prescriptions_table.setItem(row, 0, QTableWidgetItem(str(prescription.id)))
            
            # Visit ID
            self.prescriptions_table.setItem(row, 1, QTableWidgetItem(str(prescription.visit_id)))
            
            # Patient
            patient_name = f"{prescription.visit.patient.first_name} {prescription.visit.patient.last_name}" if prescription.visit and prescription.visit.patient else "N/A"
            self.prescriptions_table.setItem(row, 2, QTableWidgetItem(patient_name))
            
            # Doctor
            doctor_name = f"Dr. {prescription.visit.doctor.first_name} {prescription.visit.doctor.last_name}" if prescription.visit and prescription.visit.doctor else "N/A"
            self.prescriptions_table.setItem(row, 3, QTableWidgetItem(doctor_name))
            
            # Medication
            medication = prescription.medicament.nom_com if prescription.medicament else "N/A"
            self.prescriptions_table.setItem(row, 4, QTableWidgetItem(medication))
            
            # Dosage Instructions
            dosage = prescription.dosage_instructions[:50] + "..." if len(prescription.dosage_instructions) > 50 else prescription.dosage_instructions
            self.prescriptions_table.setItem(row, 5, QTableWidgetItem(dosage))
            
            # Quantity
            self.prescriptions_table.setItem(row, 6, QTableWidgetItem(str(prescription.quantity)))
            
            # Created
            created = prescription.created_at.strftime("%Y-%m-%d %H:%M") if prescription.created_at else "N/A"
            self.prescriptions_table.setItem(row, 7, QTableWidgetItem(created))
            
            # Store prescription ID in first column for reference
            self.prescriptions_table.item(row, 0).setData(Qt.ItemDataRole.UserRole, prescription.id)
    
    def filter_prescriptions(self):
        """Filter prescriptions based on search criteria"""
        search_text = self.search_input.text().lower()
        visit_filter = self.visit_filter.currentText()
        
        filtered_prescriptions = []
        
        for prescription in self.prescriptions:
            # Text search
            if search_text:
                searchable_text = f"{prescription.medicament.nom_com if prescription.medicament else ''} {prescription.dosage_instructions}".lower()
                if prescription.visit and prescription.visit.patient:
                    searchable_text += f" {prescription.visit.patient.first_name} {prescription.visit.patient.last_name}".lower()
                if search_text not in searchable_text:
                    continue
            
            # Visit filter
            if visit_filter != "All Visits" and str(prescription.visit_id) != visit_filter:
                continue
            
            filtered_prescriptions.append(prescription)
        
        self.populate_table(filtered_prescriptions)
        self.status_label.setText(f"Showing {len(filtered_prescriptions)} of {len(self.prescriptions)} prescriptions")
    
    def on_selection_changed(self):
        """Handle selection change"""
        current_row = self.prescriptions_table.currentRow()
        if current_row >= 0:
            item = self.prescriptions_table.item(current_row, 0)
            if item:
                prescription_id = item.data(Qt.ItemDataRole.UserRole)
                if prescription_id:
                    self.prescription_selected.emit(prescription_id)
        
        # Enable/disable action buttons
        has_selection = current_row >= 0
        self.edit_prescription_btn.setEnabled(has_selection)
        self.delete_prescription_btn.setEnabled(has_selection)
    
    def on_double_click(self, item):
        """Handle double click"""
        self.edit_selected_prescription()
    
    def new_prescription(self):
        """Create new prescription"""
        # TODO: Open prescription creation dialog
        QMessageBox.information(self, "New Prescription", "Prescription creation dialog will be implemented here.")
    
    def edit_selected_prescription(self):
        """Edit selected prescription"""
        current_row = self.prescriptions_table.currentRow()
        if current_row >= 0:
            item = self.prescriptions_table.item(current_row, 0)
            if item:
                prescription_id = item.data(Qt.ItemDataRole.UserRole)
                if prescription_id:
                    self.prescription_edit_requested.emit(prescription_id)
    
    def delete_selected_prescription(self):
        """Delete selected prescription"""
        current_row = self.prescriptions_table.currentRow()
        if current_row >= 0:
            reply = QMessageBox.question(
                self, "Confirm Delete", 
                "Are you sure you want to delete this prescription?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # TODO: Implement prescription deletion
                QMessageBox.information(self, "Delete Prescription", "Prescription deletion will be implemented here.")
                self.load_prescriptions()  # Refresh table
    
    def get_selected_prescription_id(self) -> Optional[int]:
        """Get the currently selected prescription ID"""
        current_row = self.prescriptions_table.currentRow()
        if current_row >= 0:
            item = self.prescriptions_table.item(current_row, 0)
            if item:
                return item.data(Qt.ItemDataRole.UserRole)
        return None
