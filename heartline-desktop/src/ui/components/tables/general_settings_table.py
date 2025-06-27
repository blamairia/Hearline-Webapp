"""
General Settings Table Widget for Heartline Desktop Application

This widget displays general settings in a table format with search and filtering capabilities.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QHeaderView, QLineEdit, QLabel, QMessageBox,
    QComboBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import List, Optional

from src.models.complete_models import GeneralSettings
from src.core.database import db_manager
from src.ui.styles import AppColors, AppStyles

class GeneralSettingsTableWidget(QWidget):
    """Widget for displaying and managing general_settings table"""
    
    # Signals
    settings_selected = pyqtSignal(int)  # Emitted when settings is selected
    settings_edit_requested = pyqtSignal(int)  # Emitted when edit is requested
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings: List[GeneralSettings] = []
        self.setup_ui()
        self.setup_connections()
        self.load_settings()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Apply comprehensive styling to the whole widget
        self.setStyleSheet(AppStyles.APP_STYLE)
        
        # Title
        title_label = QLabel("⚙️ General Settings")
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
        self.search_input.setPlaceholderText("Search settings...")
        filter_layout.addWidget(self.search_input)
        
        # Refresh button
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.load_settings)
        filter_layout.addWidget(self.refresh_btn)
        
        # Add button
        self.add_btn = QPushButton("➕ Add Settings")
        self.add_btn.clicked.connect(self.add_settings)
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
            "ID", "Default Appt Duration", "Appt Interval", "Weekend Appts", 
            "Currency", "Date Format", "Auto Backup", "Created", "Updated"
        ]
        
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Default Appt Duration
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Appt Interval
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Weekend Appts
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Currency
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Date Format
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Auto Backup
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)  # Created
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents)  # Updated
        
        # Set row selection behavior
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        
        # Apply table styling
        self.table.setStyleSheet(AppStyles.get_table_style())
        # Make table headers bold
        header = self.table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.search_input.textChanged.connect(self.filter_table)
        self.table.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
    
    def load_settings(self):
        """Load settings from database"""
        try:
            self.status_label.setText("Loading general settings...")
            
            # Get database session
            with db_manager.get_session() as session:
                # Query settings using SQLAlchemy
                settings_query = session.query(GeneralSettings).order_by(GeneralSettings.id).all()
                
                # Extract data from SQLAlchemy objects before session closes
                self.settings = []
                for setting in settings_query:
                    setting_data = {
                        'id': setting.id,
                        'default_appointment_duration': setting.default_appointment_duration,
                        'appointment_interval': setting.appointment_interval,
                        'weekend_appointments': setting.weekend_appointments,
                        'currency': setting.currency,
                        'date_format': setting.date_format,
                        'auto_backup': setting.auto_backup,
                        'created_at': setting.created_at,
                        'updated_at': setting.updated_at
                    }
                    self.settings.append(setting_data)
            
            self.populate_table()
            self.status_label.setText(f"✅ Loaded {len(self.settings)} settings records")
            
        except Exception as e:
            self.status_label.setText(f"❌ Error loading settings: {str(e)}")
            QMessageBox.critical(self, "Database Error", f"Failed to load general settings:\n{str(e)}")
    
    def populate_table(self):
        """Populate table with settings data"""
        self.table.setRowCount(len(self.settings))
        
        for row, settings in enumerate(self.settings):
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(settings['id'])))
            
            # Default Appointment Duration
            duration = str(settings['default_appointment_duration']) if settings['default_appointment_duration'] else ""
            self.table.setItem(row, 1, QTableWidgetItem(duration))
            
            # Appointment Interval
            interval = str(settings['appointment_interval']) if settings['appointment_interval'] else ""
            self.table.setItem(row, 2, QTableWidgetItem(interval))
            
            # Weekend Appointments
            weekend = "Yes" if settings['weekend_appointments'] else "No"
            self.table.setItem(row, 3, QTableWidgetItem(weekend))
            
            # Currency
            self.table.setItem(row, 4, QTableWidgetItem(settings['currency'] or ""))
            
            # Date Format
            self.table.setItem(row, 5, QTableWidgetItem(settings['date_format'] or ""))
            
            # Auto Backup
            backup = "Yes" if settings['auto_backup'] else "No"
            self.table.setItem(row, 6, QTableWidgetItem(backup))
            
            # Created At
            created_str = settings['created_at'].strftime("%Y-%m-%d %H:%M") if settings['created_at'] else ""
            self.table.setItem(row, 7, QTableWidgetItem(created_str))
            
            # Updated At
            updated_str = settings['updated_at'].strftime("%Y-%m-%d %H:%M") if settings['updated_at'] else ""
            self.table.setItem(row, 8, QTableWidgetItem(updated_str))
    
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
        settings_id = int(self.table.item(row, 0).text())
        self.settings_edit_requested.emit(settings_id)
    
    def on_selection_changed(self):
        """Handle selection change"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            settings_id = int(self.table.item(current_row, 0).text())
            self.settings_selected.emit(settings_id)
    
    def add_settings(self):
        """Add new settings"""
        # This will be implemented when we add CRUD functionality
        QMessageBox.information(self, "Add Settings", "Add settings functionality will be implemented in the next phase.")
    
    def get_selected_settings_id(self) -> Optional[int]:
        """Get the ID of currently selected settings"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            return int(self.table.item(current_row, 0).text())
        return None
    
    def refresh_data(self):
        """Refresh the settings data"""
        self.load_settings()
