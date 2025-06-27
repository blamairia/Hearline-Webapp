"""
Medicaments Table Widget for Heartline Desktop Application

This widget displays all medicaments in a table format with search and filtering capabilities.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QHeaderView, QLineEdit, QLabel, QMessageBox,
    QComboBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import List, Optional

from src.models.complete_models import Medicament
from src.core.database import db_manager

class MedicamentsTableWidget(QWidget):
    """Widget for displaying and managing medicaments table"""
    
    # Signals
    medicament_selected = pyqtSignal(str)  # Emitted when medicament is selected (uses num_enr)
    medicament_edit_requested = pyqtSignal(str)  # Emitted when edit is requested
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.medicaments: List[Medicament] = []
        self.setup_ui()
        self.setup_connections()
        self.load_medicaments()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("💊 Medicaments Database")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2196F3; margin: 10px;")
        layout.addWidget(title_label)
        
        # Search and filter section
        filter_frame = QFrame()
        filter_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        filter_layout = QHBoxLayout(filter_frame)
        
        # Search box
        filter_layout.addWidget(QLabel("🔍 Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, DCI, or registration number...")
        filter_layout.addWidget(self.search_input)
        
        # Unit filter
        filter_layout.addWidget(QLabel("Unit:"))
        self.unit_filter = QComboBox()
        self.unit_filter.addItem("All Units")
        filter_layout.addWidget(self.unit_filter)
        
        # Action buttons
        filter_layout.addStretch()
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.new_medicament_btn = QPushButton("➕ New Medicament")
        self.edit_medicament_btn = QPushButton("✏️ Edit")
        self.view_prescriptions_btn = QPushButton("📋 View Prescriptions")
        
        self.refresh_btn.setObjectName("primary-button")
        self.new_medicament_btn.setObjectName("success-button")
        self.edit_medicament_btn.setObjectName("primary-button")
        self.view_prescriptions_btn.setObjectName("primary-button")
        
        filter_layout.addWidget(self.refresh_btn)
        filter_layout.addWidget(self.new_medicament_btn)
        filter_layout.addWidget(self.edit_medicament_btn)
        filter_layout.addWidget(self.view_prescriptions_btn)
        
        layout.addWidget(filter_frame)
        
        # Medicaments table
        self.setup_table()
        layout.addWidget(self.medicaments_table)
        
        # Status bar
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #666; padding: 5px;")
        layout.addWidget(self.status_label)
    
    def setup_table(self):
        """Setup the medicaments table"""
        # Define columns
        self.columns = [
            ("Registration #", 120),
            ("Commercial Name", 200),
            ("DCI Name", 200),
            ("Dosage", 100),
            ("Unit", 80),
            ("Prescriptions", 100)
        ]
        
        self.medicaments_table = QTableWidget()
        self.medicaments_table.setColumnCount(len(self.columns))
        
        # Set headers and column widths
        headers = []
        for i, (header, width) in enumerate(self.columns):
            headers.append(header)
            self.medicaments_table.setColumnWidth(i, width)
        
        self.medicaments_table.setHorizontalHeaderLabels(headers)
        
        # Table properties
        self.medicaments_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.medicaments_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.medicaments_table.setAlternatingRowColors(True)
        self.medicaments_table.setSortingEnabled(True)
        
        # Make table headers bold
        header = self.medicaments_table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.search_input.textChanged.connect(self.filter_medicaments)
        self.unit_filter.currentTextChanged.connect(self.filter_medicaments)
        self.refresh_btn.clicked.connect(self.load_medicaments)
        self.new_medicament_btn.clicked.connect(self.new_medicament)
        self.edit_medicament_btn.clicked.connect(self.edit_selected_medicament)
        self.view_prescriptions_btn.clicked.connect(self.view_prescriptions)
        self.medicaments_table.itemSelectionChanged.connect(self.on_selection_changed)
        self.medicaments_table.itemDoubleClicked.connect(self.on_double_click)
    
    def load_medicaments(self):
        """Load all medicaments from database"""
        try:
            self.status_label.setText("Loading medicaments...")
            
            with db_manager.get_session() as session:
                medicaments = session.query(Medicament).order_by(Medicament.nom_com).all()
                self.medicaments = medicaments
                self.populate_table(medicaments)
                self.load_unit_filter()
                
            self.status_label.setText(f"Loaded {len(medicaments)} medicaments")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load medicaments:\n{str(e)}")
            self.status_label.setText("Error loading medicaments")
    
    def load_unit_filter(self):
        """Load unique units for filter"""
        units = set(med.unite for med in self.medicaments if med.unite)
        self.unit_filter.clear()
        self.unit_filter.addItem("All Units")
        self.unit_filter.addItems(sorted(units))
    
    def populate_table(self, medicaments: List[Medicament]):
        """Populate table with medicament data"""
        self.medicaments_table.setRowCount(len(medicaments))
        
        for row, medicament in enumerate(medicaments):
            # Registration Number
            self.medicaments_table.setItem(row, 0, QTableWidgetItem(medicament.num_enr))
            
            # Commercial Name
            self.medicaments_table.setItem(row, 1, QTableWidgetItem(medicament.nom_com))
            
            # DCI Name
            self.medicaments_table.setItem(row, 2, QTableWidgetItem(medicament.nom_dci))
            
            # Dosage
            self.medicaments_table.setItem(row, 3, QTableWidgetItem(medicament.dosage))
            
            # Unit
            self.medicaments_table.setItem(row, 4, QTableWidgetItem(medicament.unite))
            
            # Prescription count (placeholder - would need to count from prescriptions table)
            self.medicaments_table.setItem(row, 5, QTableWidgetItem("0"))  # TODO: Count actual prescriptions
            
            # Store medicament num_enr in first column for reference
            self.medicaments_table.item(row, 0).setData(Qt.ItemDataRole.UserRole, medicament.num_enr)
    
    def filter_medicaments(self):
        """Filter medicaments based on search criteria"""
        search_text = self.search_input.text().lower()
        unit_filter = self.unit_filter.currentText()
        
        filtered_medicaments = []
        
        for medicament in self.medicaments:
            # Text search
            if search_text:
                searchable_text = f"{medicament.num_enr} {medicament.nom_com} {medicament.nom_dci} {medicament.dosage}".lower()
                if search_text not in searchable_text:
                    continue
            
            # Unit filter
            if unit_filter != "All Units" and medicament.unite != unit_filter:
                continue
            
            filtered_medicaments.append(medicament)
        
        self.populate_table(filtered_medicaments)
        self.status_label.setText(f"Showing {len(filtered_medicaments)} of {len(self.medicaments)} medicaments")
    
    def on_selection_changed(self):
        """Handle selection change"""
        current_row = self.medicaments_table.currentRow()
        if current_row >= 0:
            item = self.medicaments_table.item(current_row, 0)
            if item:
                medicament_num_enr = item.data(Qt.ItemDataRole.UserRole)
                if medicament_num_enr:
                    self.medicament_selected.emit(medicament_num_enr)
        
        # Enable/disable action buttons
        has_selection = current_row >= 0
        self.edit_medicament_btn.setEnabled(has_selection)
        self.view_prescriptions_btn.setEnabled(has_selection)
    
    def on_double_click(self, item):
        """Handle double click"""
        self.edit_selected_medicament()
    
    def new_medicament(self):
        """Create new medicament"""
        # TODO: Open medicament creation dialog
        QMessageBox.information(self, "New Medicament", "Medicament creation dialog will be implemented here.")
    
    def edit_selected_medicament(self):
        """Edit selected medicament"""
        current_row = self.medicaments_table.currentRow()
        if current_row >= 0:
            item = self.medicaments_table.item(current_row, 0)
            if item:
                medicament_num_enr = item.data(Qt.ItemDataRole.UserRole)
                if medicament_num_enr:
                    self.medicament_edit_requested.emit(medicament_num_enr)
    
    def view_prescriptions(self):
        """View prescriptions for selected medicament"""
        current_row = self.medicaments_table.currentRow()
        if current_row >= 0:
            # TODO: Open prescriptions view for this medicament
            QMessageBox.information(self, "View Prescriptions", "Prescriptions view will be implemented here.")
    
    def get_selected_medicament_num_enr(self) -> Optional[str]:
        """Get the currently selected medicament registration number"""
        current_row = self.medicaments_table.currentRow()
        if current_row >= 0:
            item = self.medicaments_table.item(current_row, 0)
            if item:
                return item.data(Qt.ItemDataRole.UserRole)
        return None
