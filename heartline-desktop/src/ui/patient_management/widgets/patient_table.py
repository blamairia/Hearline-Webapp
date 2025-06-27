"""
Advanced Patient Table Widget with CRUD Operations

This widget provides a comprehensive table view for patient management with
advanced features like search, filtering, sorting, context menus, and bulk operations.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QHeaderView, QLineEdit, QLabel, QMessageBox,
    QComboBox, QFrame, QMenu, QDialog, QCheckBox, QSpinBox,
    QDateEdit, QProgressDialog, QInputDialog, QFileDialog,
    QSplitter, QGroupBox, QFormLayout, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QThread, pyqtSlot
from PyQt6.QtGui import QFont, QAction, QKeySequence, QShortcut, QColor, QBrush
from typing import List, Optional, Set
from datetime import datetime, date
import csv
import json

from src.models.complete_models import Patient
from src.core.database import db_manager
from src.ui.styles import AppColors, AppStyles


class PatientTableWidget(QWidget):
    """Advanced patient table widget with comprehensive features"""
    
    # Signals
    patient_selected = pyqtSignal(int)  # Emitted when patient is selected
    patient_edit_requested = pyqtSignal(int)  # Emitted when edit is requested
    patient_view_requested = pyqtSignal(int)  # Emitted when view details is requested
    patients_changed = pyqtSignal()  # Emitted when patient list changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.patients: List[Patient] = []
        self.filtered_patients: List[Patient] = []
        self.selected_patients: Set[int] = set()
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.apply_filters)
        
        self.setup_ui()
        self.setup_connections()
        self.setup_shortcuts()
        self.load_patients()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Apply comprehensive styling to the whole widget - same as doctor table
        self.setStyleSheet(AppStyles.APP_STYLE)
        
        # Title and toolbar
        header_layout = QHBoxLayout()
        
        title_label = QLabel("👥 Patients Management")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {AppColors.PRIMARY}; margin: 5px;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Quick stats
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet(f"color: {AppColors.TEXT_SECONDARY}; font-size: 12px;")
        header_layout.addWidget(self.stats_label)
        
        layout.addLayout(header_layout)
        
        # Search and filter section
        self.filter_frame = self.create_filter_section()
        layout.addWidget(self.filter_frame)
        
        # Main content area with splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side - Table
        table_widget = QWidget()
        table_layout = QVBoxLayout(table_widget)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        
        # Action buttons
        self.new_patient_btn = QPushButton("➕ New Patient")
        self.new_patient_btn.setStyleSheet(AppStyles.PRIMARY_BUTTON_STYLE)
        self.new_patient_btn.setToolTip("Add a new patient (Ctrl+N)")
        
        self.edit_patient_btn = QPushButton("✏️ Edit")
        self.edit_patient_btn.setEnabled(False)
        self.edit_patient_btn.setToolTip("Edit selected patient (Ctrl+E)")
        
        self.view_patient_btn = QPushButton("👁️ View")
        self.view_patient_btn.setEnabled(False)
        self.view_patient_btn.setToolTip("View patient details (Ctrl+I)")
        
        self.delete_patient_btn = QPushButton("🗑️ Delete")
        self.delete_patient_btn.setEnabled(False)
        self.delete_patient_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; }")
        self.delete_patient_btn.setToolTip("Delete selected patient(s) (Delete)")
        
        toolbar_layout.addWidget(self.new_patient_btn)
        toolbar_layout.addWidget(self.edit_patient_btn)
        toolbar_layout.addWidget(self.view_patient_btn)
        toolbar_layout.addWidget(self.delete_patient_btn)
        
        # Bulk actions
        toolbar_layout.addWidget(QLabel("|"))
        
        self.select_all_btn = QPushButton("✅ Select All")
        self.select_all_btn.setToolTip("Select all patients (Ctrl+A)")
        
        self.clear_selection_btn = QPushButton("❌ Clear Selection")
        self.clear_selection_btn.setToolTip("Clear selection (Esc)")
        
        self.bulk_actions_btn = QPushButton("📦 Bulk Actions")
        self.bulk_actions_btn.setEnabled(False)
        
        toolbar_layout.addWidget(self.select_all_btn)
        toolbar_layout.addWidget(self.clear_selection_btn)
        toolbar_layout.addWidget(self.bulk_actions_btn)
        
        # Export/Import
        toolbar_layout.addWidget(QLabel("|"))
        
        self.export_btn = QPushButton("📤 Export")
        self.export_btn.setToolTip("Export patient data")
        
        self.import_btn = QPushButton("📥 Import")
        self.import_btn.setToolTip("Import patient data")
        
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.setToolTip("Refresh patient list (F5)")
        
        toolbar_layout.addWidget(self.export_btn)
        toolbar_layout.addWidget(self.import_btn)
        toolbar_layout.addWidget(self.refresh_btn)
        toolbar_layout.addStretch()
        
        table_layout.addLayout(toolbar_layout)
        
        # Patients table
        self.patients_table = QTableWidget()
        self.setup_table()
        table_layout.addWidget(self.patients_table)
        
        splitter.addWidget(table_widget)
        
        # Right side - Quick info panel (collapsible)
        self.info_panel = self.create_info_panel()
        splitter.addWidget(self.info_panel)
        
        # Set initial splitter sizes (table takes 70%, info panel 30%)
        splitter.setSizes([700, 300])
        
        layout.addWidget(splitter)
        
        # Status bar
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Ready")
        self.selection_label = QLabel("")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        status_layout.addWidget(self.selection_label)
        layout.addLayout(status_layout)
    
    def create_filter_section(self) -> QFrame:
        """Create the search and filter section"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {AppColors.BACKGROUND};
                border: 1px solid {AppColors.BORDER};
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        
        layout = QHBoxLayout(frame)
        
        # Search section
        search_group = QGroupBox("🔍 Search")
        search_layout = QHBoxLayout(search_group)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, phone, email, or ID...")
        self.search_input.setMinimumWidth(300)
        search_layout.addWidget(self.search_input)
        
        self.search_clear_btn = QPushButton("❌")
        self.search_clear_btn.setMaximumWidth(30)
        self.search_clear_btn.setToolTip("Clear search")
        search_layout.addWidget(self.search_clear_btn)
        
        layout.addWidget(search_group)
        
        # Filters section
        filters_group = QGroupBox("🎯 Filters")
        filters_layout = QHBoxLayout(filters_group)
        
        # Gender filter
        filters_layout.addWidget(QLabel("Gender:"))
        self.gender_filter = QComboBox()
        self.gender_filter.addItems(["All", "Male", "Female", "Other"])
        filters_layout.addWidget(self.gender_filter)
        
        # Age range filter
        filters_layout.addWidget(QLabel("Age:"))
        self.age_min_spin = QSpinBox()
        self.age_min_spin.setRange(0, 150)
        self.age_min_spin.setSpecialValueText("Min")
        self.age_min_spin.setValue(0)
        filters_layout.addWidget(self.age_min_spin)
        
        filters_layout.addWidget(QLabel("to"))
        self.age_max_spin = QSpinBox()
        self.age_max_spin.setRange(0, 150)
        self.age_max_spin.setSpecialValueText("Max")
        self.age_max_spin.setValue(150)
        filters_layout.addWidget(self.age_max_spin)
        
        # Insurance filter
        filters_layout.addWidget(QLabel("Insurance:"))
        self.insurance_filter = QComboBox()
        self.insurance_filter.addItems(["All", "Insured", "Uninsured"])
        filters_layout.addWidget(self.insurance_filter)
        
        # Clear filters button
        self.clear_filters_btn = QPushButton("🔄 Clear Filters")
        filters_layout.addWidget(self.clear_filters_btn)
        
        layout.addWidget(filters_group)
        
        # View options
        view_group = QGroupBox("👁️ View")
        view_layout = QHBoxLayout(view_group)
        
        self.show_inactive_cb = QCheckBox("Show Inactive")
        view_layout.addWidget(self.show_inactive_cb)
        
        self.rows_per_page_combo = QComboBox()
        self.rows_per_page_combo.addItems(["25", "50", "100", "All"])
        self.rows_per_page_combo.setCurrentText("50")
        view_layout.addWidget(QLabel("Rows:"))
        view_layout.addWidget(self.rows_per_page_combo)
        
        layout.addWidget(view_group)
        
        return frame
    
    def create_info_panel(self) -> QWidget:
        """Create the patient info panel"""
        panel = QWidget()
        panel.setMaximumWidth(300)
        panel.setStyleSheet(f"""
            QWidget {{
                background-color: {AppColors.BACKGROUND};
                border: 1px solid {AppColors.BORDER};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(panel)
        
        # Panel title
        title_label = QLabel("📊 Patient Info")
        title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {AppColors.PRIMARY}; padding: 10px;")
        layout.addWidget(title_label)
        
        # Selected patient info
        self.info_scroll = QScrollArea()
        self.info_widget = QWidget()
        self.info_layout = QVBoxLayout(self.info_widget)
        
        self.no_selection_label = QLabel("Select a patient to view details")
        self.no_selection_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_selection_label.setStyleSheet(f"color: {AppColors.TEXT_SECONDARY}; padding: 20px;")
        self.info_layout.addWidget(self.no_selection_label)
        
        self.info_scroll.setWidget(self.info_widget)
        self.info_scroll.setWidgetResizable(True)
        layout.addWidget(self.info_scroll)
        
        return panel
    
    def setup_table(self):
        """Setup the patients table"""
        # Enhanced columns with more patient information
        self.columns = [
            ("", 30),  # Checkbox column
            ("ID", 60),
            ("Name", 150),
            ("Age", 50),
            ("Gender", 70),
            ("Phone", 120),
            ("Email", 180),
            ("Insurance", 120),
            ("Last Visit", 100),
            ("Emergency Contact", 150),
            ("Status", 80),
            ("Created", 100)
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
        self.patients_table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        self.patients_table.setAlternatingRowColors(True)
        self.patients_table.setSortingEnabled(True)
        self.patients_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        
        # Make first column (checkbox) non-sortable
        self.patients_table.horizontalHeader().setSortIndicatorShown(True)
        self.patients_table.horizontalHeader().sectionClicked.connect(self.on_header_clicked)
        
        # Table styling - use same as doctor management
        self.patients_table.setStyleSheet(AppStyles.get_table_style())
        
        # Make table headers bold and centered - same as doctor table  
        header = self.patients_table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(True)
    
    def setup_connections(self):
        """Setup signal connections"""
        # Search and filters
        self.search_input.textChanged.connect(self.on_search_changed)
        self.search_clear_btn.clicked.connect(self.clear_search)
        self.gender_filter.currentTextChanged.connect(self.apply_filters)
        self.age_min_spin.valueChanged.connect(self.apply_filters)
        self.age_max_spin.valueChanged.connect(self.apply_filters)
        self.insurance_filter.currentTextChanged.connect(self.apply_filters)
        self.clear_filters_btn.clicked.connect(self.clear_filters)
        self.show_inactive_cb.toggled.connect(self.apply_filters)
        self.rows_per_page_combo.currentTextChanged.connect(self.apply_filters)
        
        # Table interactions
        self.patients_table.itemSelectionChanged.connect(self.on_selection_changed)
        self.patients_table.itemDoubleClicked.connect(self.on_double_click)
        self.patients_table.customContextMenuRequested.connect(self.show_context_menu)
        self.patients_table.cellChanged.connect(self.on_cell_changed)
        
        # Toolbar buttons
        self.new_patient_btn.clicked.connect(self.new_patient)
        self.edit_patient_btn.clicked.connect(self.edit_selected_patient)
        self.view_patient_btn.clicked.connect(self.view_selected_patient)
        self.delete_patient_btn.clicked.connect(self.delete_selected_patients)
        self.select_all_btn.clicked.connect(self.select_all_patients)
        self.clear_selection_btn.clicked.connect(self.clear_selection)
        self.bulk_actions_btn.clicked.connect(self.show_bulk_actions_menu)
        self.export_btn.clicked.connect(self.export_patients)
        self.import_btn.clicked.connect(self.import_patients)
        self.refresh_btn.clicked.connect(self.load_patients)
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Create new patient
        new_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        new_shortcut.activated.connect(self.new_patient)
        
        # Edit patient
        edit_shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        edit_shortcut.activated.connect(self.edit_selected_patient)
        
        # View patient details
        view_shortcut = QShortcut(QKeySequence("Ctrl+I"), self)
        view_shortcut.activated.connect(self.view_selected_patient)
        
        # Delete patient
        delete_shortcut = QShortcut(QKeySequence("Delete"), self)
        delete_shortcut.activated.connect(self.delete_selected_patients)
        
        # Select all
        select_all_shortcut = QShortcut(QKeySequence("Ctrl+A"), self)
        select_all_shortcut.activated.connect(self.select_all_patients)
        
        # Clear selection
        clear_shortcut = QShortcut(QKeySequence("Escape"), self)
        clear_shortcut.activated.connect(self.clear_selection)
        
        # Refresh
        refresh_shortcut = QShortcut(QKeySequence("F5"), self)
        refresh_shortcut.activated.connect(self.load_patients)
        
        # Find
        find_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        find_shortcut.activated.connect(lambda: self.search_input.setFocus())
    
    def load_patients(self):
        """Load all patients from database"""
        try:
            self.status_label.setText("Loading patients...")
            
            with db_manager.get_session() as session:
                patients_query = session.query(Patient).order_by(Patient.last_name, Patient.first_name)
                patients = patients_query.all()
                
                # Extract all data before session closes
                self.patients = []
                for patient in patients:
                    # Create a simple data structure with all needed info
                    patient_data = type('PatientData', (), {})()
                    patient_data.id = patient.id
                    patient_data.first_name = patient.first_name
                    patient_data.last_name = patient.last_name
                    patient_data.age = patient.age  # This will calculate from date_of_birth
                    patient_data.gender = patient.gender
                    patient_data.phone = patient.phone
                    patient_data.email = patient.email
                    patient_data.insurance_provider = patient.insurance_provider
                    patient_data.emergency_contact_name = patient.emergency_contact_name
                    patient_data.emergency_contact_phone = patient.emergency_contact_phone
                    patient_data.created_at = patient.created_at
                    patient_data.date_of_birth = patient.date_of_birth
                    patient_data.address = patient.address
                    patient_data.city = patient.city
                    patient_data.state = patient.state
                    patient_data.allergies = patient.allergies
                    patient_data.chronic_conditions = patient.chronic_conditions
                    patient_data.is_active = getattr(patient, 'is_active', True)
                    
                    self.patients.append(patient_data)
                
                self.apply_filters()
                self.update_stats()
                
            self.status_label.setText(f"Loaded {len(self.patients)} patients")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load patients:\n{str(e)}")
            self.status_label.setText("Error loading patients")
    
    def apply_filters(self):
        """Apply search and filter criteria"""
        search_text = self.search_input.text().lower().strip()
        gender_filter = self.gender_filter.currentText()
        age_min = self.age_min_spin.value() if self.age_min_spin.value() > 0 else 0
        age_max = self.age_max_spin.value() if self.age_max_spin.value() < 150 else 999
        insurance_filter = self.insurance_filter.currentText()
        show_inactive = self.show_inactive_cb.isChecked()
        
        filtered_patients = []
        
        for patient in self.patients:
            # Activity filter
            if not show_inactive and not getattr(patient, 'is_active', True):
                continue
            
            # Text search
            if search_text:
                searchable_text = f"{patient.first_name or ''} {patient.last_name or ''} {patient.phone or ''} {patient.email or ''} {patient.id}".lower()
                if search_text not in searchable_text:
                    continue
            
            # Gender filter
            if gender_filter != "All" and patient.gender != gender_filter:
                continue
            
            # Age filter
            if patient.age is not None:
                if not (age_min <= patient.age <= age_max):
                    continue
            
            # Insurance filter
            if insurance_filter == "Insured" and not patient.insurance_provider:
                continue
            elif insurance_filter == "Uninsured" and patient.insurance_provider:
                continue
            
            filtered_patients.append(patient)
        
        self.filtered_patients = filtered_patients
        self.populate_table(filtered_patients)
        self.update_filter_stats()
    
    def populate_table(self, patients: List[Patient]):
        """Populate table with patient data"""
        # Handle pagination
        rows_per_page = self.rows_per_page_combo.currentText()
        if rows_per_page != "All":
            patients = patients[:int(rows_per_page)]
        
        self.patients_table.setRowCount(len(patients))
        
        for row, patient in enumerate(patients):
            # Checkbox column
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.CheckState.Checked if patient.id in self.selected_patients else Qt.CheckState.Unchecked)
            self.patients_table.setItem(row, 0, checkbox_item)
            
            # ID
            id_item = QTableWidgetItem(str(patient.id))
            id_item.setData(Qt.ItemDataRole.UserRole, patient.id)
            self.patients_table.setItem(row, 1, id_item)
            
            # Name
            full_name = f"{patient.first_name or ''} {patient.last_name or ''}".strip()
            name_item = QTableWidgetItem(full_name)
            name_item.setToolTip(full_name)
            self.patients_table.setItem(row, 2, name_item)
            
            # Age
            age_item = QTableWidgetItem(str(patient.age) if patient.age else "N/A")
            self.patients_table.setItem(row, 3, age_item)
            
            # Gender
            gender_item = QTableWidgetItem(patient.gender or "N/A")
            # Color code gender
            if patient.gender == "Male":
                gender_item.setBackground(QBrush(QColor("#e3f2fd")))
            elif patient.gender == "Female":
                gender_item.setBackground(QBrush(QColor("#fce4ec")))
            self.patients_table.setItem(row, 4, gender_item)
            
            # Phone
            phone_item = QTableWidgetItem(patient.phone or "N/A")
            phone_item.setToolTip(patient.phone or "No phone number")
            self.patients_table.setItem(row, 5, phone_item)
            
            # Email
            email_item = QTableWidgetItem(patient.email or "N/A")
            email_item.setToolTip(patient.email or "No email address")
            self.patients_table.setItem(row, 6, email_item)
            
            # Insurance
            insurance_item = QTableWidgetItem(patient.insurance_provider or "Uninsured")
            # Color code insurance status
            if patient.insurance_provider:
                insurance_item.setBackground(QBrush(QColor("#e8f5e8")))
            else:
                insurance_item.setBackground(QBrush(QColor("#fff3e0")))
            self.patients_table.setItem(row, 7, insurance_item)
            
            # Last Visit (placeholder)
            last_visit_item = QTableWidgetItem("N/A")
            self.patients_table.setItem(row, 8, last_visit_item)
            
            # Emergency Contact
            emergency_contact = patient.emergency_contact_name or "N/A"
            emergency_item = QTableWidgetItem(emergency_contact)
            emergency_item.setToolTip(f"Name: {patient.emergency_contact_name or 'N/A'}\nPhone: {patient.emergency_contact_phone or 'N/A'}")
            self.patients_table.setItem(row, 9, emergency_item)
            
            # Status
            status = "Active" if getattr(patient, 'is_active', True) else "Inactive"
            status_item = QTableWidgetItem(status)
            if status == "Active":
                status_item.setBackground(QBrush(QColor("#e8f5e8")))
            else:
                status_item.setBackground(QBrush(QColor("#ffebee")))
            self.patients_table.setItem(row, 10, status_item)
            
            # Created
            created_str = patient.created_at.strftime("%Y-%m-%d") if patient.created_at else "N/A"
            created_item = QTableWidgetItem(created_str)
            created_item.setToolTip(patient.created_at.strftime("%Y-%m-%d %H:%M:%S") if patient.created_at else "Unknown")
            self.patients_table.setItem(row, 11, created_item)
    
    def update_stats(self):
        """Update patient statistics"""
        total = len(self.patients)
        male_count = sum(1 for p in self.patients if p.gender == "Male")
        female_count = sum(1 for p in self.patients if p.gender == "Female")
        insured_count = sum(1 for p in self.patients if p.insurance_provider)
        
        stats_text = f"Total: {total} | Male: {male_count} | Female: {female_count} | Insured: {insured_count}"
        self.stats_label.setText(stats_text)
    
    def update_filter_stats(self):
        """Update filtered results statistics"""
        showing = len(self.filtered_patients)
        total = len(self.patients)
        
        if showing == total:
            self.status_label.setText(f"Showing all {total} patients")
        else:
            self.status_label.setText(f"Showing {showing} of {total} patients")
    
    def on_search_changed(self):
        """Handle search text change with debouncing"""
        self.search_timer.stop()
        self.search_timer.start(300)  # 300ms delay
    
    def clear_search(self):
        """Clear search input"""
        self.search_input.clear()
        self.apply_filters()
    
    def clear_filters(self):
        """Clear all filters"""
        self.search_input.clear()
        self.gender_filter.setCurrentIndex(0)
        self.age_min_spin.setValue(0)
        self.age_max_spin.setValue(150)
        self.insurance_filter.setCurrentIndex(0)
        self.show_inactive_cb.setChecked(False)
        self.apply_filters()
    
    def on_selection_changed(self):
        """Handle table selection change"""
        selected_rows = set()
        
        for i in range(self.patients_table.rowCount()):
            checkbox_item = self.patients_table.item(i, 0)
            if checkbox_item and checkbox_item.checkState() == Qt.CheckState.Checked:
                id_item = self.patients_table.item(i, 1)
                if id_item:
                    patient_id = id_item.data(Qt.ItemDataRole.UserRole)
                    if patient_id:
                        selected_rows.add(patient_id)
        
        self.selected_patients = selected_rows
        
        # Update button states
        has_selection = len(selected_rows) > 0
        single_selection = len(selected_rows) == 1
        
        self.edit_patient_btn.setEnabled(single_selection)
        self.view_patient_btn.setEnabled(single_selection)
        self.delete_patient_btn.setEnabled(has_selection)
        self.bulk_actions_btn.setEnabled(has_selection)
        
        # Update selection label
        if len(selected_rows) == 0:
            self.selection_label.setText("")
        elif len(selected_rows) == 1:
            self.selection_label.setText("1 patient selected")
        else:
            self.selection_label.setText(f"{len(selected_rows)} patients selected")
        
        # Update info panel
        if single_selection:
            patient_id = next(iter(selected_rows))
            self.update_info_panel(patient_id)
            self.patient_selected.emit(patient_id)
        else:
            self.clear_info_panel()
    
    def on_cell_changed(self, row: int, column: int):
        """Handle cell change (for checkbox column)"""
        if column == 0:  # Checkbox column
            self.on_selection_changed()
    
    def on_double_click(self, item):
        """Handle double click on table item"""
        if item and item.column() != 0:  # Don't trigger on checkbox
            self.view_selected_patient()
    
    def on_header_clicked(self, logical_index: int):
        """Handle header click for sorting"""
        if logical_index == 0:  # Checkbox column
            # Toggle select all
            if len(self.selected_patients) == len(self.filtered_patients):
                self.clear_selection()
            else:
                self.select_all_patients()
    
    def show_context_menu(self, position):
        """Show context menu for table"""
        item = self.patients_table.itemAt(position)
        if not item:
            return
        
        menu = QMenu(self)
        
        # Patient actions
        view_action = menu.addAction("👁️ View Details")
        edit_action = menu.addAction("✏️ Edit Patient")
        menu.addSeparator()
        
        # Selection actions
        select_action = menu.addAction("✅ Select")
        deselect_action = menu.addAction("❌ Deselect")
        menu.addSeparator()
        
        # Data actions
        export_action = menu.addAction("📤 Export Selected")
        menu.addSeparator()
        delete_action = menu.addAction("🗑️ Delete")
        
        # Execute menu
        action = menu.exec(self.patients_table.mapToGlobal(position))
        
        if action == view_action:
            self.view_selected_patient()
        elif action == edit_action:
            self.edit_selected_patient()
        elif action == select_action:
            row = item.row()
            checkbox_item = self.patients_table.item(row, 0)
            if checkbox_item:
                checkbox_item.setCheckState(Qt.CheckState.Checked)
        elif action == deselect_action:
            row = item.row()
            checkbox_item = self.patients_table.item(row, 0)
            if checkbox_item:
                checkbox_item.setCheckState(Qt.CheckState.Unchecked)
        elif action == export_action:
            self.export_selected_patients()
        elif action == delete_action:
            self.delete_selected_patients()
    
    def update_info_panel(self, patient_id: int):
        """Update the info panel with patient details"""
        # Find patient in filtered list
        patient = None
        for p in self.filtered_patients:
            if p.id == patient_id:
                patient = p
                break
        
        if not patient:
            self.clear_info_panel()
            return
        
        # Clear existing content
        while self.info_layout.count():
            child = self.info_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Patient name and basic info
        name_label = QLabel(f"{patient.first_name} {patient.last_name}")
        name_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        name_label.setStyleSheet(f"color: {AppColors.PRIMARY}; padding: 5px;")
        self.info_layout.addWidget(name_label)
        
        # Basic details
        details = []
        if patient.age:
            details.append(f"Age: {patient.age}")
        if patient.gender:
            details.append(f"Gender: {patient.gender}")
        
        if details:
            details_label = QLabel(" • ".join(details))
            details_label.setStyleSheet(f"color: {AppColors.TEXT_SECONDARY}; padding: 2px 5px;")
            self.info_layout.addWidget(details_label)
        
        # Contact information
        contact_group = QGroupBox("📞 Contact")
        contact_layout = QVBoxLayout(contact_group)
        
        if patient.phone:
            phone_label = QLabel(f"Phone: {patient.phone}")
            contact_layout.addWidget(phone_label)
        
        if patient.email:
            email_label = QLabel(f"Email: {patient.email}")
            contact_layout.addWidget(email_label)
        
        if patient.address or patient.city or patient.state:
            address_parts = []
            if patient.address:
                address_parts.append(patient.address)
            if patient.city:
                address_parts.append(patient.city)
            if patient.state:
                address_parts.append(patient.state)
            
            address_label = QLabel(f"Address: {', '.join(address_parts)}")
            address_label.setWordWrap(True)
            contact_layout.addWidget(address_label)
        
        self.info_layout.addWidget(contact_group)
        
        # Medical information
        medical_group = QGroupBox("🏥 Medical")
        medical_layout = QVBoxLayout(medical_group)
        
        if patient.insurance_provider:
            insurance_label = QLabel(f"Insurance: {patient.insurance_provider}")
            medical_layout.addWidget(insurance_label)
        
        if patient.allergies:
            allergies_label = QLabel(f"Allergies: {patient.allergies[:50]}{'...' if len(patient.allergies) > 50 else ''}")
            allergies_label.setWordWrap(True)
            medical_layout.addWidget(allergies_label)
        
        if patient.chronic_conditions:
            conditions_label = QLabel(f"Conditions: {patient.chronic_conditions[:50]}{'...' if len(patient.chronic_conditions) > 50 else ''}")
            conditions_label.setWordWrap(True)
            medical_layout.addWidget(conditions_label)
        
        self.info_layout.addWidget(medical_group)
        
        # Emergency contact
        if patient.emergency_contact_name or patient.emergency_contact_phone:
            emergency_group = QGroupBox("🚨 Emergency Contact")
            emergency_layout = QVBoxLayout(emergency_group)
            
            if patient.emergency_contact_name:
                name_label = QLabel(f"Name: {patient.emergency_contact_name}")
                emergency_layout.addWidget(name_label)
            
            if patient.emergency_contact_phone:
                phone_label = QLabel(f"Phone: {patient.emergency_contact_phone}")
                emergency_layout.addWidget(phone_label)
            
            self.info_layout.addWidget(emergency_group)
        
        self.info_layout.addStretch()
    
    def clear_info_panel(self):
        """Clear the info panel"""
        while self.info_layout.count():
            child = self.info_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Recreate the no_selection_label since it was deleted
        self.no_selection_label = QLabel("Select a patient to view details")
        self.no_selection_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_selection_label.setStyleSheet(f"color: {AppColors.TEXT_SECONDARY}; padding: 20px;")
        self.info_layout.addWidget(self.no_selection_label)
    
    def select_all_patients(self):
        """Select all visible patients"""
        for i in range(self.patients_table.rowCount()):
            checkbox_item = self.patients_table.item(i, 0)
            if checkbox_item:
                checkbox_item.setCheckState(Qt.CheckState.Checked)
        self.on_selection_changed()
    
    def clear_selection(self):
        """Clear all selections"""
        for i in range(self.patients_table.rowCount()):
            checkbox_item = self.patients_table.item(i, 0)
            if checkbox_item:
                checkbox_item.setCheckState(Qt.CheckState.Unchecked)
        self.selected_patients.clear()
        self.on_selection_changed()
    
    def new_patient(self):
        """Create new patient"""
        # This will be handled by the main widget
        pass
    
    def edit_selected_patient(self):
        """Edit selected patient"""
        if len(self.selected_patients) == 1:
            patient_id = next(iter(self.selected_patients))
            self.patient_edit_requested.emit(patient_id)
    
    def view_selected_patient(self):
        """View selected patient details"""
        if len(self.selected_patients) == 1:
            patient_id = next(iter(self.selected_patients))
            self.patient_view_requested.emit(patient_id)
    
    def delete_selected_patients(self):
        """Delete selected patients"""
        if not self.selected_patients:
            return
        
        count = len(self.selected_patients)
        patient_names = []
        
        # Get patient names for confirmation
        for patient in self.filtered_patients:
            if patient.id in self.selected_patients:
                patient_names.append(f"{patient.first_name} {patient.last_name}")
        
        if count == 1:
            message = f"Are you sure you want to delete patient {patient_names[0]}?"
        else:
            message = f"Are you sure you want to delete {count} patients?\n\n" + "\n".join(patient_names[:5])
            if len(patient_names) > 5:
                message += f"\n... and {len(patient_names) - 5} more"
        
        reply = QMessageBox.question(
            self, "Confirm Delete", message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                with db_manager.get_session() as session:
                    for patient_id in self.selected_patients:
                        patient = session.query(Patient).filter(Patient.id == patient_id).first()
                        if patient:
                            session.delete(patient)
                    session.commit()
                
                QMessageBox.information(self, "Success", f"Successfully deleted {count} patient(s)")
                self.patients_changed.emit()
                self.load_patients()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete patients:\n{str(e)}")
    
    def show_bulk_actions_menu(self):
        """Show bulk actions menu"""
        if not self.selected_patients:
            return
        
        menu = QMenu(self)
        
        export_action = menu.addAction("📤 Export Selected")
        print_action = menu.addAction("🖨️ Print Selected")
        menu.addSeparator()
        email_action = menu.addAction("📧 Send Email")
        menu.addSeparator()
        activate_action = menu.addAction("✅ Mark as Active")
        deactivate_action = menu.addAction("❌ Mark as Inactive")
        menu.addSeparator()
        delete_action = menu.addAction("🗑️ Delete Selected")
        
        action = menu.exec(self.bulk_actions_btn.mapToGlobal(self.bulk_actions_btn.rect().bottomLeft()))
        
        if action == export_action:
            self.export_selected_patients()
        elif action == print_action:
            self.print_selected_patients()
        elif action == email_action:
            self.send_email_to_selected()
        elif action == activate_action:
            self.update_patient_status(True)
        elif action == deactivate_action:
            self.update_patient_status(False)
        elif action == delete_action:
            self.delete_selected_patients()
    
    def export_patients(self):
        """Export all patients to CSV"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Patients", "patients.csv", "CSV Files (*.csv)")
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Write headers
                    headers = [
                        'ID', 'First Name', 'Last Name', 'Age', 'Gender', 'Phone', 'Email',
                        'Address', 'City', 'State', 'Insurance Provider', 'Emergency Contact',
                        'Emergency Phone', 'Created'
                    ]
                    writer.writerow(headers)
                    
                    # Write patient data
                    for patient in self.filtered_patients:
                        row = [
                            patient.id,
                            patient.first_name or '',
                            patient.last_name or '',
                            patient.age or '',
                            patient.gender or '',
                            patient.phone or '',
                            patient.email or '',
                            patient.address or '',
                            patient.city or '',
                            patient.state or '',
                            patient.insurance_provider or '',
                            patient.emergency_contact_name or '',
                            patient.emergency_contact_phone or '',
                            patient.created_at.strftime('%Y-%m-%d %H:%M:%S') if patient.created_at else ''
                        ]
                        writer.writerow(row)
                
                QMessageBox.information(self, "Success", f"Exported {len(self.filtered_patients)} patients to {filename}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export patients:\n{str(e)}")
    
    def export_selected_patients(self):
        """Export selected patients"""
        if not self.selected_patients:
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Selected Patients", "selected_patients.csv", "CSV Files (*.csv)")
        
        if filename:
            try:
                selected_patient_data = [p for p in self.filtered_patients if p.id in self.selected_patients]
                
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Write headers
                    headers = [
                        'ID', 'First Name', 'Last Name', 'Age', 'Gender', 'Phone', 'Email',
                        'Address', 'City', 'State', 'Insurance Provider', 'Emergency Contact',
                        'Emergency Phone', 'Created'
                    ]
                    writer.writerow(headers)
                    
                    # Write selected patient data
                    for patient in selected_patient_data:
                        row = [
                            patient.id,
                            patient.first_name or '',
                            patient.last_name or '',
                            patient.age or '',
                            patient.gender or '',
                            patient.phone or '',
                            patient.email or '',
                            patient.address or '',
                            patient.city or '',
                            patient.state or '',
                            patient.insurance_provider or '',
                            patient.emergency_contact_name or '',
                            patient.emergency_contact_phone or '',
                            patient.created_at.strftime('%Y-%m-%d %H:%M:%S') if patient.created_at else ''
                        ]
                        writer.writerow(row)
                
                QMessageBox.information(self, "Success", f"Exported {len(selected_patient_data)} selected patients to {filename}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export selected patients:\n{str(e)}")
    
    def import_patients(self):
        """Import patients from CSV"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Import Patients", "", "CSV Files (*.csv)")
        
        if filename:
            QMessageBox.information(self, "Import", "Import functionality will be implemented")
    
    def print_selected_patients(self):
        """Print selected patients"""
        QMessageBox.information(self, "Print", "Print functionality will be implemented")
    
    def send_email_to_selected(self):
        """Send email to selected patients"""
        QMessageBox.information(self, "Email", "Email functionality will be implemented")
    
    def update_patient_status(self, is_active: bool):
        """Update status of selected patients"""
        if not self.selected_patients:
            return
        
        status_text = "active" if is_active else "inactive"
        count = len(self.selected_patients)
        
        reply = QMessageBox.question(
            self, "Confirm Status Change",
            f"Mark {count} patient(s) as {status_text}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                with db_manager.get_session() as session:
                    for patient_id in self.selected_patients:
                        patient = session.query(Patient).filter(Patient.id == patient_id).first()
                        if patient:
                            patient.is_active = is_active
                    session.commit()
                
                QMessageBox.information(self, "Success", f"Updated status for {count} patient(s)")
                self.patients_changed.emit()
                self.load_patients()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update patient status:\n{str(e)}")
    
    def get_selected_patient_ids(self) -> List[int]:
        """Get list of selected patient IDs"""
        return list(self.selected_patients)
    
    def refresh(self):
        """Refresh the patients data"""
        self.load_patients()
