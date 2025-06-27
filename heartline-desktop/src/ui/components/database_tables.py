"""
Database Tables Management Widget for Heartline Desktop Application

This widget provides access to all database tables with tabbed interface for complete data management.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTabWidget, 
    QLabel, QFrame, QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from .tables import (
    PatientsTableWidget, DoctorsTableWidget, AppointmentsTableWidget,
    VisitsTableWidget, WaitingListTableWidget, PrescriptionsTableWidget,
    UsersTableWidget, MedicamentsTableWidget, VisitDocumentsTableWidget,
    ClinicInfoTableWidget, GeneralSettingsTableWidget
)

class DatabaseTablesWidget(QWidget):
    """Widget for managing all database tables with tabbed interface"""
    
    # Signals
    data_updated = pyqtSignal(str)  # Emitted when data is updated (table name)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table_widgets = {}  # Initialize before setup_ui
        self.setup_ui()
        self.setup_connections()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Title section
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-bottom: 2px solid #2196F3;
                padding: 16px;
                margin-bottom: 0;
            }
        """)
        title_layout = QHBoxLayout(title_frame)
        
        title_label = QLabel("🗃️ Database Tables Management")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1976D2; margin: 0;")
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()
        
        # Refresh all button
        self.refresh_all_btn = QPushButton("🔄 Refresh All")
        self.refresh_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.refresh_all_btn.clicked.connect(self.refresh_all_tables)
        title_layout.addWidget(self.refresh_all_btn)
        
        layout.addWidget(title_frame)
        
        # Info section
        info_label = QLabel(
            "View and manage all database tables. Each tab represents a table in the database. "
            "Use the search functionality within each table to find specific records."
        )
        info_label.setStyleSheet("color: #666; margin: 10px; padding: 5px;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Create tabbed interface
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #c0c0c0;
                background-color: white;
            }
            QTabWidget::tab-bar {
                left: 5px;
            }
            QTabBar::tab {
                background-color: #e1e1e1;
                padding: 8px 16px;
                margin-right: 2px;
                border: 1px solid #c0c0c0;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 1px solid white;
            }
            QTabBar::tab:hover {
                background-color: #f0f0f0;
            }
        """)
        
        self.create_table_tabs()
        layout.addWidget(self.tab_widget)
        
        # Status section
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background-color: #f9f9f9;
                border-top: 1px solid #e0e0e0;
                padding: 8px;
            }
        """)
        status_layout = QHBoxLayout(status_frame)
        
        self.status_label = QLabel("Ready - All tables loaded")
        self.status_label.setStyleSheet("color: #666;")
        status_layout.addWidget(self.status_label)
        
        status_layout.addStretch()
        
        # Record count label
        self.record_count_label = QLabel("")
        self.record_count_label.setStyleSheet("color: #2196F3; font-weight: bold;")
        status_layout.addWidget(self.record_count_label)
        
        layout.addWidget(status_frame)
    
    def create_table_tabs(self):
        """Create tabs for all database tables"""
        
        # Define all tables with their widgets and display names
        tables_config = [
            # Core Management Tables
            ("👥 Patients", PatientsTableWidget, "Core patient records"),
            ("👨‍⚕️ Doctors", DoctorsTableWidget, "Medical staff information"),
            ("📅 Appointments", AppointmentsTableWidget, "Scheduled appointments"),
            ("🏥 Visits", VisitsTableWidget, "Patient visit records"),
            ("⏳ Waiting List", WaitingListTableWidget, "Current waiting patients"),
            
            # Medical & Documentation
            ("💊 Prescriptions", PrescriptionsTableWidget, "Prescribed medications"),
            ("📄 Visit Documents", VisitDocumentsTableWidget, "Attached documents"),
            ("💉 Medicaments", MedicamentsTableWidget, "Available medications"),
            
            # System & Configuration
            ("👤 Users", UsersTableWidget, "System users"),
            ("🏥 Clinic Info", ClinicInfoTableWidget, "Clinic information"),
            ("⚙️ General Settings", GeneralSettingsTableWidget, "System settings"),
        ]
        
        # Store table widgets for easy access
        self.table_widgets = {}
        
        for tab_name, widget_class, description in tables_config:
            # Create the table widget
            table_widget = widget_class()
            
            # Create a container with description
            container = QWidget()
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            
            # Add description label
            desc_label = QLabel(f"📝 {description}")
            desc_label.setStyleSheet("""
                QLabel {
                    background-color: #e3f2fd;
                    padding: 8px;
                    color: #1976D2;
                    border-left: 4px solid #2196F3;
                    margin-bottom: 5px;
                }
            """)
            container_layout.addWidget(desc_label)
            
            # Add the table widget
            container_layout.addWidget(table_widget)
            
            # Add tab
            self.tab_widget.addTab(container, tab_name)
            
            # Store reference
            table_name = tab_name.split(' ', 1)[1].lower().replace(' ', '_')  # Extract clean name
            self.table_widgets[table_name] = table_widget
        
        # Connect tab change to update status
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
    
    def setup_connections(self):
        """Setup signal connections"""
        # Connect signals from table widgets if they have them
        for table_widget in self.table_widgets.values():
            if hasattr(table_widget, 'data_updated'):
                table_widget.data_updated.connect(self.on_table_data_updated)
    
    def refresh_all_tables(self):
        """Refresh data in all tables"""
        try:
            self.status_label.setText("🔄 Refreshing all tables...")
            self.refresh_all_btn.setEnabled(False)
            
            # Refresh each table widget
            for table_widget in self.table_widgets.values():
                if hasattr(table_widget, 'refresh_data'):
                    table_widget.refresh_data()
                elif hasattr(table_widget, 'load_data'):
                    table_widget.load_data()
                elif hasattr(table_widget, 'load_patients'):
                    table_widget.load_patients()
                elif hasattr(table_widget, 'load_doctors'):
                    table_widget.load_doctors()
                elif hasattr(table_widget, 'load_appointments'):
                    table_widget.load_appointments()
                elif hasattr(table_widget, 'load_visits'):
                    table_widget.load_visits()
                elif hasattr(table_widget, 'load_waiting_list'):
                    table_widget.load_waiting_list()
                elif hasattr(table_widget, 'load_prescriptions'):
                    table_widget.load_prescriptions()
                elif hasattr(table_widget, 'load_users'):
                    table_widget.load_users()
                elif hasattr(table_widget, 'load_medicaments'):
                    table_widget.load_medicaments()
                elif hasattr(table_widget, 'load_visit_documents'):
                    table_widget.load_visit_documents()
                elif hasattr(table_widget, 'load_clinic_infos'):
                    table_widget.load_clinic_infos()
                elif hasattr(table_widget, 'load_settings'):
                    table_widget.load_settings()
                elif hasattr(table_widget, 'load_sessions'):
                    table_widget.load_sessions()
            
            self.status_label.setText("✅ All tables refreshed successfully")
            self.update_record_counts()
            
        except Exception as e:
            self.status_label.setText(f"❌ Error refreshing tables: {str(e)}")
            QMessageBox.critical(self, "Refresh Error", f"Failed to refresh all tables:\n{str(e)}")
        
        finally:
            self.refresh_all_btn.setEnabled(True)
    
    def on_tab_changed(self, index):
        """Handle tab change"""
        if index >= 0:
            tab_name = self.tab_widget.tabText(index)
            self.status_label.setText(f"Viewing {tab_name}")
            self.update_record_counts()
    
    def on_table_data_updated(self, table_name):
        """Handle data update from table widgets"""
        self.status_label.setText(f"✅ {table_name} data updated")
        self.data_updated.emit(table_name)
        self.update_record_counts()
    
    def update_record_counts(self):
        """Update the record count display for current tab"""
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            # Get the current table widget
            container = self.tab_widget.widget(current_index)
            if container and container.layout():
                table_widget = None
                for i in range(container.layout().count()):
                    item = container.layout().itemAt(i)
                    if item and item.widget():
                        widget = item.widget()
                        # Check if this is a table widget (has a table attribute)
                        if hasattr(widget, 'table'):
                            table_widget = widget
                            break
                
                if table_widget and hasattr(table_widget, 'table'):
                    total_rows = table_widget.table.rowCount()
                    visible_rows = 0
                    for row in range(total_rows):
                        if not table_widget.table.isRowHidden(row):
                            visible_rows += 1
                    
                    if visible_rows != total_rows:
                        self.record_count_label.setText(f"Showing {visible_rows} of {total_rows} records")
                    else:
                        self.record_count_label.setText(f"{total_rows} records")
                else:
                    self.record_count_label.setText("")
    
    def get_current_table_widget(self):
        """Get the currently active table widget"""
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            container = self.tab_widget.widget(current_index)
            if container and container.layout():
                for i in range(container.layout().count()):
                    item = container.layout().itemAt(i)
                    if item and item.widget() and hasattr(item.widget(), 'table'):
                        return item.widget()
        return None
    
    def switch_to_table(self, table_name):
        """Switch to a specific table tab"""
        for i in range(self.tab_widget.count()):
            tab_text = self.tab_widget.tabText(i)
            if table_name.lower() in tab_text.lower():
                self.tab_widget.setCurrentIndex(i)
                return True
        return False
