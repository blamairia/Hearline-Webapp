"""
Main Appointment Management Widget

This widget provides comprehensive appointment management with enhanced features.
Integrates the appointment table and dialog for a complete user experience.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QFrame, QMessageBox, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import Optional

from src.ui.styles import AppColors, AppStyles
from src.ui.components.tables.appointments_table import AppointmentsTableWidget
from .dialogs.appointment_dialog import AppointmentDialog

class AppointmentManagementWidget(QWidget):
    """Main appointment management widget with enhanced features"""
    
    # Signals
    appointment_created = pyqtSignal(int)  # Emitted when appointment is created
    appointment_updated = pyqtSignal(int)  # Emitted when appointment is updated
    appointment_deleted = pyqtSignal(int)  # Emitted when appointment is deleted
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_connections()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Apply styles
        self.setStyleSheet(AppStyles.APP_STYLE)
        
        # Header section
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        header_layout = QVBoxLayout(header_frame)
        
        # Title
        title_label = QLabel("📅 Appointment Management")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {AppColors.PRIMARY};
                margin: 10px 0px;
                background-color: transparent;
                border: none;
            }}
        """)
        header_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel("Manage patient appointments, scheduling, and calendar")
        desc_label.setFont(QFont("Segoe UI", 12))
        desc_label.setStyleSheet(f"""
            QLabel {{
                color: {AppColors.TEXT_SECONDARY};
                margin-bottom: 10px;
                background-color: transparent;
                border: none;
            }}
        """)
        header_layout.addWidget(desc_label)
        
        # Quick action buttons
        action_layout = QHBoxLayout()
        
        self.new_appointment_btn = QPushButton("➕ New Appointment")
        self.new_appointment_btn.setStyleSheet(AppStyles.PRIMARY_BUTTON_STYLE)
        self.new_appointment_btn.setMinimumHeight(40)
        self.new_appointment_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        action_layout.addWidget(self.new_appointment_btn)
        
        self.quick_schedule_btn = QPushButton("🕒 Quick Schedule")
        self.quick_schedule_btn.setStyleSheet(AppStyles.SECONDARY_BUTTON_STYLE)
        self.quick_schedule_btn.setMinimumHeight(40)
        action_layout.addWidget(self.quick_schedule_btn)
        
        self.calendar_view_btn = QPushButton("📅 Calendar View")
        self.calendar_view_btn.setStyleSheet(AppStyles.SECONDARY_BUTTON_STYLE)
        self.calendar_view_btn.setMinimumHeight(40)
        action_layout.addWidget(self.calendar_view_btn)
        
        action_layout.addStretch()
        
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.setStyleSheet(AppStyles.SECONDARY_BUTTON_STYLE)
        self.refresh_btn.setMinimumHeight(40)
        action_layout.addWidget(self.refresh_btn)
        
        header_layout.addLayout(action_layout)
        layout.addWidget(header_frame)
        
        # Create tabs for different views
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {AppColors.BORDER};
                background-color: {AppColors.BACKGROUND};
                border-radius: 4px;
            }}
            QTabBar::tab {{
                background-color: {AppColors.BACKGROUND_SECONDARY};
                color: {AppColors.TEXT_PRIMARY};
                padding: 12px 20px;
                margin-right: 2px;
                border: 1px solid {AppColors.BORDER};
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font-weight: 500;
            }}
            QTabBar::tab:selected {{
                background-color: {AppColors.PRIMARY};
                color: {AppColors.TEXT_ON_PRIMARY};
                border-bottom: 1px solid {AppColors.PRIMARY};
                font-weight: bold;
            }}
            QTabBar::tab:hover {{
                background-color: {AppColors.HOVER};
                color: {AppColors.TEXT_PRIMARY};
            }}
            QTabBar::tab:selected:hover {{
                background-color: {AppColors.PRIMARY_DARK};
                color: {AppColors.TEXT_ON_PRIMARY};
            }}
        """)
        
        # Appointments Table Tab
        self.appointments_table = AppointmentsTableWidget()
        self.tab_widget.addTab(self.appointments_table, "📋 Appointments List")
        
        # TODO: Add calendar view tab in future
        # self.calendar_widget = AppointmentCalendarWidget()
        # self.tab_widget.addTab(self.calendar_widget, "📅 Calendar View")
        
        layout.addWidget(self.tab_widget)
        
        # Status bar
        self.status_label = QLabel("Ready - Appointment Management")
        self.status_label.setStyleSheet("color: #666; padding: 5px; font-size: 12px;")
        layout.addWidget(self.status_label)
    
    def setup_connections(self):
        """Setup signal connections"""
        # Button connections
        self.new_appointment_btn.clicked.connect(self.create_new_appointment)
        self.quick_schedule_btn.clicked.connect(self.quick_schedule)
        self.calendar_view_btn.clicked.connect(self.show_calendar_view)
        self.refresh_btn.clicked.connect(self.refresh_data)
        
        # Table signals
        self.appointments_table.appointment_selected.connect(self.on_appointment_selected)
        self.appointments_table.appointment_edit_requested.connect(self.edit_appointment)
    
    def create_new_appointment(self):
        """Create a new appointment"""
        try:
            dialog = AppointmentDialog(parent=self)
            dialog.appointment_saved.connect(self.on_appointment_saved)
            
            if dialog.exec() == AppointmentDialog.DialogCode.Accepted:
                self.status_label.setText("✅ New appointment created successfully")
            else:
                self.status_label.setText("❌ Appointment creation cancelled")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create appointment dialog:\n{str(e)}")
            self.status_label.setText(f"❌ Error: {str(e)}")
    
    def edit_appointment(self, appointment_id: int):
        """Edit an existing appointment"""
        try:
            dialog = AppointmentDialog(appointment_id=appointment_id, parent=self)
            dialog.appointment_saved.connect(self.on_appointment_saved)
            
            if dialog.exec() == AppointmentDialog.DialogCode.Accepted:
                self.status_label.setText("✅ Appointment updated successfully")
            else:
                self.status_label.setText("❌ Appointment edit cancelled")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to edit appointment:\n{str(e)}")
            self.status_label.setText(f"❌ Error: {str(e)}")
    
    def quick_schedule(self):
        """Quick scheduling dialog - simplified appointment creation"""
        # TODO: Implement quick schedule dialog
        QMessageBox.information(self, "Quick Schedule", "Quick scheduling feature coming soon!")
        self.status_label.setText("ℹ️ Quick schedule feature coming soon")
    
    def show_calendar_view(self):
        """Switch to calendar view"""
        # TODO: Implement calendar view
        QMessageBox.information(self, "Calendar View", "Calendar view feature coming soon!")
        self.status_label.setText("ℹ️ Calendar view feature coming soon")
    
    def refresh_data(self):
        """Refresh all appointment data"""
        try:
            self.appointments_table.load_appointments()
            self.status_label.setText("✅ Data refreshed successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to refresh data:\n{str(e)}")
            self.status_label.setText(f"❌ Refresh failed: {str(e)}")
    
    def on_appointment_selected(self, appointment_id: int):
        """Handle appointment selection"""
        self.status_label.setText(f"Selected appointment ID: {appointment_id}")
    
    def on_appointment_saved(self, appointment_id: int):
        """Handle appointment save event"""
        # Refresh the table to show updated data
        self.refresh_data()
        
        # Emit signals
        if hasattr(self, '_is_editing') and self._is_editing:
            self.appointment_updated.emit(appointment_id)
        else:
            self.appointment_created.emit(appointment_id)
    
    def new_appointment(self):
        """Public method to create new appointment (for external calls)"""
        self.create_new_appointment()
