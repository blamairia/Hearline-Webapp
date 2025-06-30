"""
Main Doctor Management Widget

Simple doctor management with basic table view and CRUD operations.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import Optional

from .widgets.doctor_table import DoctorTableWidget
from .dialogs.doctor_dialog import DoctorDialog
from src.ui.styles import AppColors, AppStyles


class DoctorManagementWidget(QWidget):
    """Simple doctor management widget"""
    
    # Signals
    doctor_selected = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_connections()
        self.load_initial_data()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Header with title and main actions
        header_frame = self.create_header()
        layout.addWidget(header_frame)
        
        # Main table view
        self.table_widget = DoctorTableWidget()
        layout.addWidget(self.table_widget)
        
        # Status bar
        self.status_frame = self.create_status_bar()
        layout.addWidget(self.status_frame)
    
    def create_header(self) -> QFrame:
        """Create the header with title and main actions"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {AppColors.BACKGROUND};
                border: 1px solid {AppColors.BORDER};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        
        layout = QHBoxLayout(frame)
        
        # Title section
        title_layout = QVBoxLayout()
        
        title_label = QLabel("👨‍⚕️ Doctor Management System")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {AppColors.PRIMARY};")
        title_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Simple doctor information management")
        subtitle_label.setFont(QFont("Segoe UI", 10))
        subtitle_label.setStyleSheet(f"color: {AppColors.TEXT_SECONDARY};")
        title_layout.addWidget(subtitle_label)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Main action buttons
        self.new_doctor_btn = QPushButton("➕ New Doctor")
        self.new_doctor_btn.setStyleSheet(AppStyles.PRIMARY_BUTTON_STYLE)
        self.new_doctor_btn.setToolTip("Add a new doctor")
        layout.addWidget(self.new_doctor_btn)
        
        self.edit_doctor_btn = QPushButton("✏️ Edit Doctor")
        self.edit_doctor_btn.setStyleSheet(AppStyles.SECONDARY_BUTTON_STYLE)
        self.edit_doctor_btn.setToolTip("Edit selected doctor")
        self.edit_doctor_btn.setEnabled(False)
        layout.addWidget(self.edit_doctor_btn)
        
        return frame
    
    def create_status_bar(self) -> QFrame:
        """Create the status bar"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {AppColors.BACKGROUND_SECONDARY};
                border: 1px solid {AppColors.BORDER};
                border-radius: 4px;
                padding: 5px;
            }}
        """)
        
        layout = QHBoxLayout(frame)
        
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(f"color: {AppColors.TEXT_SECONDARY}; font-size: 12px;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        # Quick stats
        self.stats_label = QLabel("Doctors: 0")
        self.stats_label.setStyleSheet(f"color: {AppColors.TEXT_SECONDARY}; font-size: 12px;")
        layout.addWidget(self.stats_label)
        
        return frame
    
    def setup_connections(self):
        """Setup signal connections"""
        # Header buttons
        self.new_doctor_btn.clicked.connect(self.create_new_doctor)
        self.edit_doctor_btn.clicked.connect(self.edit_selected_doctor)
        
        # Table signals
        self.table_widget.doctor_selected.connect(self.on_doctor_selected)
        self.table_widget.doctor_edit_requested.connect(self.edit_doctor)
    
    def load_initial_data(self):
        """Load initial data"""
        self.table_widget.load_doctors()
        self.update_stats()
    
    def update_stats(self):
        """Update statistics display"""
        doctor_count = len(self.table_widget.doctors)
        self.stats_label.setText(f"Doctors: {doctor_count}")
        
        active_count = sum(1 for d in self.table_widget.doctors if d.get('status') == 'Active')
        self.status_label.setText(f"Active: {active_count} | Total: {doctor_count}")
    
    def on_doctor_selected(self, doctor_id: int):
        """Handle doctor selection"""
        self.edit_doctor_btn.setEnabled(True)
        self.doctor_selected.emit(doctor_id)
    
    def create_new_doctor(self):
        """Create a new doctor"""
        dialog = DoctorDialog(parent=self)
        dialog.doctor_saved.connect(self.on_doctor_saved)
        dialog.exec()
    
    def edit_selected_doctor(self):
        """Edit the selected doctor"""
        doctor_id = self.table_widget.get_selected_doctor_id()
        if doctor_id:
            self.edit_doctor(doctor_id)
    
    def edit_doctor(self, doctor_id: int):
        """Edit a specific doctor"""
        dialog = DoctorDialog(doctor_id=doctor_id, parent=self)
        dialog.doctor_saved.connect(self.on_doctor_saved)
        dialog.exec()
    
    def on_doctor_saved(self, doctor_id: int):
        """Handle doctor saved signal"""
        self.table_widget.load_doctors()
        self.update_stats()
        self.status_label.setText("Doctor saved successfully")
    
    def refresh_data(self):
        """Refresh all data"""
        self.table_widget.refresh()
        self.update_stats()
    
    def get_selected_doctor_id(self) -> Optional[int]:
        """Get the currently selected doctor ID"""
        return self.table_widget.get_selected_doctor_id()
