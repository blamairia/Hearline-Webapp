"""
Clinic Info Table Widget for Heartline Desktop Application

This widget displays clinic information in a table format with search and filtering capabilities.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QHeaderView, QLineEdit, QLabel, QMessageBox,
    QComboBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import List, Optional

from src.models.complete_models import ClinicInfo
from src.core.database import db_manager

class ClinicInfoTableWidget(QWidget):
    """Widget for displaying and managing clinic_info table"""
    
    # Signals
    clinic_info_selected = pyqtSignal(int)  # Emitted when clinic info is selected
    clinic_info_edit_requested = pyqtSignal(int)  # Emitted when edit is requested
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clinic_infos: List[ClinicInfo] = []
        self.setup_ui()
        self.setup_connections()
        self.load_clinic_infos()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("🏥 Clinic Information")
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
        self.search_input.setPlaceholderText("Search by name, phone, email, or address...")
        filter_layout.addWidget(self.search_input)
        
        # Refresh button
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.load_clinic_infos)
        filter_layout.addWidget(self.refresh_btn)
        
        # Add button
        self.add_btn = QPushButton("➕ Add Clinic Info")
        self.add_btn.clicked.connect(self.add_clinic_info)
        filter_layout.addWidget(self.add_btn)
        
        layout.addWidget(filter_frame)
        
        # Table
        self.table = QTableWidget()
        self.setup_table()
        layout.addWidget(self.table)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #666; margin: 5px;")
        layout.addWidget(self.status_label)
    
    def setup_table(self):
        """Setup the table widget"""
        headers = [
            "ID", "Name", "Phone", "Email", "Address", 
            "Website", "Operating Hours", "Specialties", 
            "Created", "Updated"
        ]
        
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Name
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Phone
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Email
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)          # Address
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Website
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)          # Operating Hours
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Stretch)          # Specialties
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents)  # Created
        header.setSectionResizeMode(9, QHeaderView.ResizeMode.ResizeToContents)  # Updated
        
        # Set row selection behavior
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        
        # Make table headers bold
        header = self.table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.search_input.textChanged.connect(self.filter_table)
        self.table.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
    
    def load_clinic_infos(self):
        """Load clinic infos from database"""
        try:
            self.status_label.setText("Loading clinic information...")
            
            # Get database session
            with db_manager.get_session() as session:
                # Query clinic info using SQLAlchemy
                clinic_infos_query = session.query(ClinicInfo).order_by(ClinicInfo.name).all()
                
                # Extract data from SQLAlchemy objects before session closes
                self.clinic_infos = []
                for clinic_info in clinic_infos_query:
                    clinic_data = {
                        'id': clinic_info.id,
                        'name': clinic_info.name,
                        'phone': clinic_info.phone,
                        'email': clinic_info.email,
                        'address': clinic_info.address,
                        'website': clinic_info.website,
                        'operating_hours': clinic_info.operating_hours,
                        'specialties': clinic_info.specialties,
                        'created_at': clinic_info.created_at,
                        'updated_at': clinic_info.updated_at
                    }
                    self.clinic_infos.append(clinic_data)
            
            self.populate_table()
            self.status_label.setText(f"✅ Loaded {len(self.clinic_infos)} clinic info records")
            
        except Exception as e:
            self.status_label.setText(f"❌ Error loading clinic info: {str(e)}")
            QMessageBox.critical(self, "Database Error", f"Failed to load clinic information:\n{str(e)}")
    
    def populate_table(self):
        """Populate table with clinic info data"""
        self.table.setRowCount(len(self.clinic_infos))
        
        for row, clinic_info in enumerate(self.clinic_infos):
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(clinic_info['id'])))
            
            # Name
            self.table.setItem(row, 1, QTableWidgetItem(clinic_info['name'] or ""))
            
            # Phone
            self.table.setItem(row, 2, QTableWidgetItem(clinic_info['phone'] or ""))
            
            # Email
            self.table.setItem(row, 3, QTableWidgetItem(clinic_info['email'] or ""))
            
            # Address
            self.table.setItem(row, 4, QTableWidgetItem(clinic_info['address'] or ""))
            
            # Website
            self.table.setItem(row, 5, QTableWidgetItem(clinic_info['website'] or ""))
            
            # Operating Hours
            self.table.setItem(row, 6, QTableWidgetItem(clinic_info['operating_hours'] or ""))
            
            # Specialties
            self.table.setItem(row, 7, QTableWidgetItem(clinic_info['specialties'] or ""))
            
            # Created At
            created_str = clinic_info['created_at'].strftime("%Y-%m-%d") if clinic_info['created_at'] else ""
            self.table.setItem(row, 8, QTableWidgetItem(created_str))
            created_str = clinic_info.created_at.strftime("%Y-%m-%d %H:%M") if clinic_info.created_at else ""
            self.table.setItem(row, 8, QTableWidgetItem(created_str))
            
            # Updated At
            updated_str = clinic_info.updated_at.strftime("%Y-%m-%d %H:%M") if clinic_info.updated_at else ""
            self.table.setItem(row, 9, QTableWidgetItem(updated_str))
    
    def filter_table(self):
        """Filter table based on search input"""
        search_text = self.search_input.text().lower()
        
        for row in range(self.table.rowCount()):
            should_show = False
            
            # Check if search text matches any visible column
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    should_show = True
                    break
            
            self.table.setRowHidden(row, not should_show)
    
    def on_item_double_clicked(self, item):
        """Handle item double click"""
        row = item.row()
        clinic_info_id = int(self.table.item(row, 0).text())
        self.clinic_info_edit_requested.emit(clinic_info_id)
    
    def on_selection_changed(self):
        """Handle selection change"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            clinic_info_id = int(self.table.item(current_row, 0).text())
            self.clinic_info_selected.emit(clinic_info_id)
    
    def add_clinic_info(self):
        """Add new clinic info"""
        # This will be implemented when we add CRUD functionality
        QMessageBox.information(self, "Add Clinic Info", "Add clinic info functionality will be implemented in the next phase.")
    
    def get_selected_clinic_info_id(self) -> Optional[int]:
        """Get the ID of currently selected clinic info"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            return int(self.table.item(current_row, 0).text())
        return None
    
    def refresh_data(self):
        """Refresh the clinic info data"""
        self.load_clinic_infos()
