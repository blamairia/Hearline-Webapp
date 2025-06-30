"""
Main Patient Management Widget

This is the main widget that orchestrates all patient management functionality,
including table view, card view, dialogs, and CRUD operations.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget,
    QMessageBox, QFileDialog, QProgressDialog, QTabWidget, QLabel,
    QFrame, QSplitter, QButtonGroup, QToolButton, QMenu
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, pyqtSlot
from PyQt6.QtGui import QFont, QAction
from typing import Optional, List
from datetime import datetime
import os

from .widgets.patient_table import PatientTableWidget
from .widgets.patient_card import PatientCardWidget
from .dialogs.patient_dialog import PatientDialog
from .dialogs.patient_details_dialog import PatientDetailsDialog
from .utils.patient_export import PatientExporter
from .utils.patient_import import PatientImporter
from src.ui.styles import AppColors, AppStyles


class ImportWorker(QThread):
    """Worker thread for importing patients"""
    
    progress_updated = pyqtSignal(int)  # Progress percentage
    import_completed = pyqtSignal(int, int, list)  # imported, errors, error_list
    
    def __init__(self, filename: str, importer: PatientImporter):
        super().__init__()
        self.filename = filename
        self.importer = importer
    
    def run(self):
        """Run the import process"""
        try:
            self.progress_updated.emit(10)
            imported, errors, error_list = self.importer.import_patients(self.filename)
            self.progress_updated.emit(100)
            self.import_completed.emit(imported, errors, error_list)
        except Exception as e:
            self.import_completed.emit(0, 1, [str(e)])


class PatientManagementWidget(QWidget):
    """Main patient management widget with comprehensive functionality"""
    
    # Signals
    patient_selected = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_view = "table"  # "table" or "cards"
        self.exporter = PatientExporter()
        self.importer = PatientImporter()
        self.import_worker = None
        
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
        
        # Main content area
        self.stacked_widget = QStackedWidget()
        
        # Table view
        self.table_widget = PatientTableWidget()
        self.stacked_widget.addWidget(self.table_widget)
        
        # Card view
        self.card_widget = PatientCardWidget()
        self.stacked_widget.addWidget(self.card_widget)
        
        layout.addWidget(self.stacked_widget)
        
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
        
        title_label = QLabel("👥 Patient Management System")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {AppColors.PRIMARY};")
        title_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Comprehensive patient data management with advanced features")
        subtitle_label.setFont(QFont("Segoe UI", 10))
        subtitle_label.setStyleSheet(f"color: {AppColors.TEXT_SECONDARY};")
        title_layout.addWidget(subtitle_label)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # View toggle buttons
        view_group = QButtonGroup(self)
        
        self.table_view_btn = QToolButton()
        self.table_view_btn.setText("📋 Table View")
        self.table_view_btn.setCheckable(True)
        self.table_view_btn.setChecked(True)
        self.table_view_btn.setStyleSheet(AppStyles.PRIMARY_BUTTON_STYLE)
        view_group.addButton(self.table_view_btn)
        
        self.card_view_btn = QToolButton()
        self.card_view_btn.setText("🗂️ Card View")
        self.card_view_btn.setCheckable(True)
        self.card_view_btn.setStyleSheet(AppStyles.SECONDARY_BUTTON_STYLE)
        view_group.addButton(self.card_view_btn)
        
        layout.addWidget(self.table_view_btn)
        layout.addWidget(self.card_view_btn)
        
        # Main action buttons
        layout.addWidget(QLabel("|"))
        
        self.new_patient_btn = QPushButton("➕ New Patient")
        self.new_patient_btn.setStyleSheet(AppStyles.PRIMARY_BUTTON_STYLE)
        self.new_patient_btn.setToolTip("Add a new patient (Ctrl+N)")
        layout.addWidget(self.new_patient_btn)
        
        # Import/Export menu button
        self.import_export_btn = QToolButton()
        self.import_export_btn.setText("📁 Data")
        self.import_export_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.setup_import_export_menu()
        layout.addWidget(self.import_export_btn)
        
        # Settings/Tools menu
        self.tools_btn = QToolButton()
        self.tools_btn.setText("🔧 Tools")
        self.tools_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.setup_tools_menu()
        layout.addWidget(self.tools_btn)
        
        return frame
    
    def setup_import_export_menu(self):
        """Setup the import/export menu"""
        menu = QMenu(self)
        
        # Export actions
        export_menu = menu.addMenu("📤 Export")
        
        export_csv_action = export_menu.addAction("📄 Export as CSV")
        export_csv_action.triggered.connect(lambda: self.export_patients('csv'))
        
        export_json_action = export_menu.addAction("📋 Export as JSON")
        export_json_action.triggered.connect(lambda: self.export_patients('json'))
        
        if 'xlsx' in self.exporter.get_supported_formats():
            export_excel_action = export_menu.addAction("📊 Export as Excel")
            export_excel_action.triggered.connect(lambda: self.export_patients('xlsx'))
        
        if 'pdf' in self.exporter.get_supported_formats():
            export_pdf_action = export_menu.addAction("📑 Export as PDF")
            export_pdf_action.triggered.connect(lambda: self.export_patients('pdf'))
        
        export_menu.addSeparator()
        export_selected_action = export_menu.addAction("📤 Export Selected")
        export_selected_action.triggered.connect(self.export_selected_patients)
        
        # Import actions
        import_menu = menu.addMenu("📥 Import")
        
        import_csv_action = import_menu.addAction("📄 Import from CSV")
        import_csv_action.triggered.connect(lambda: self.import_patients('csv'))
        
        import_json_action = import_menu.addAction("📋 Import from JSON")
        import_json_action.triggered.connect(lambda: self.import_patients('json'))
        
        if 'xlsx' in self.importer.get_supported_formats():
            import_excel_action = import_menu.addAction("📊 Import from Excel")
            import_excel_action.triggered.connect(lambda: self.import_patients('xlsx'))
        
        import_menu.addSeparator()
        import_template_action = import_menu.addAction("📋 Download Import Template")
        import_template_action.triggered.connect(self.download_import_template)
        
        self.import_export_btn.setMenu(menu)
    
    def setup_tools_menu(self):
        """Setup the tools menu"""
        menu = QMenu(self)
        
        # Data management
        data_menu = menu.addMenu("🗃️ Data Management")
        
        cleanup_action = data_menu.addAction("🧹 Cleanup Duplicate Records")
        cleanup_action.triggered.connect(self.cleanup_duplicates)
        
        backup_action = data_menu.addAction("💾 Backup Patient Data")
        backup_action.triggered.connect(self.backup_data)
        
        # Reports
        reports_menu = menu.addMenu("📊 Reports")
        
        summary_action = reports_menu.addAction("📈 Patient Summary Report")
        summary_action.triggered.connect(self.generate_summary_report)
        
        demographics_action = reports_menu.addAction("👥 Demographics Report")
        demographics_action.triggered.connect(self.generate_demographics_report)
        
        # Settings
        menu.addSeparator()
        
        settings_action = menu.addAction("⚙️ Patient Management Settings")
        settings_action.triggered.connect(self.open_settings)
        
        self.tools_btn.setMenu(menu)
    
    def create_status_bar(self) -> QFrame:
        """Create the status bar"""
        frame = QFrame()
        frame.setMaximumHeight(30)
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {AppColors.BACKGROUND};
                border-top: 1px solid {AppColors.BORDER};
                padding: 5px;
            }}
        """)
        
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 0, 10, 0)
        
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(f"color: {AppColors.TEXT_SECONDARY};")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        self.view_info_label = QLabel("")
        self.view_info_label.setStyleSheet(f"color: {AppColors.TEXT_SECONDARY};")
        layout.addWidget(self.view_info_label)
        
        return frame
    
    def setup_connections(self):
        """Setup signal connections"""
        # View switching
        self.table_view_btn.clicked.connect(lambda: self.switch_view("table"))
        self.card_view_btn.clicked.connect(lambda: self.switch_view("cards"))
        
        # New patient
        self.new_patient_btn.clicked.connect(self.new_patient)
        
        # Table widget signals
        self.table_widget.patient_selected.connect(self.on_patient_selected)
        self.table_widget.patient_edit_requested.connect(self.edit_patient)
        self.table_widget.patient_view_requested.connect(self.view_patient_details)
        self.table_widget.patients_changed.connect(self.refresh_data)
        self.table_widget.new_patient = self.new_patient  # Override method
        
        # Card widget signals
        self.card_widget.patient_selected.connect(self.on_patient_selected)
        self.card_widget.patient_edit_requested.connect(self.edit_patient)
        self.card_widget.patient_view_requested.connect(self.view_patient_details)
    
    def load_initial_data(self):
        """Load initial patient data"""
        self.refresh_data()
    
    def switch_view(self, view_type: str):
        """Switch between table and card views"""
        if view_type == "table":
            self.stacked_widget.setCurrentWidget(self.table_widget)
            self.table_view_btn.setChecked(True)
            self.table_view_btn.setStyleSheet(AppStyles.PRIMARY_BUTTON_STYLE)
            self.card_view_btn.setStyleSheet(AppStyles.SECONDARY_BUTTON_STYLE)
            self.current_view = "table"
            self.view_info_label.setText("Table View")
        elif view_type == "cards":
            self.stacked_widget.setCurrentWidget(self.card_widget)
            self.card_view_btn.setChecked(True)
            self.card_view_btn.setStyleSheet(AppStyles.PRIMARY_BUTTON_STYLE)
            self.table_view_btn.setStyleSheet(AppStyles.SECONDARY_BUTTON_STYLE)
            self.current_view = "cards"
            self.view_info_label.setText("Card View")
            
            # Update card view with current patients
            if hasattr(self.table_widget, 'filtered_patients'):
                self.card_widget.set_patients(self.table_widget.filtered_patients)
    
    def new_patient(self):
        """Create a new patient"""
        dialog = PatientDialog(parent=self)
        dialog.patient_saved.connect(self.on_patient_saved)
        dialog.exec()
    
    def edit_patient(self, patient_id: int):
        """Edit an existing patient"""
        dialog = PatientDialog(patient_id=patient_id, parent=self)
        dialog.patient_saved.connect(self.on_patient_saved)
        dialog.exec()
    
    def view_patient_details(self, patient_id: int):
        """View patient details"""
        dialog = PatientDetailsDialog(patient_id=patient_id, parent=self)
        dialog.edit_requested.connect(self.edit_patient)
        dialog.exec()
    
    def on_patient_selected(self, patient_id: int):
        """Handle patient selection"""
        self.patient_selected.emit(patient_id)
        self.status_label.setText(f"Selected patient ID: {patient_id}")
    
    def on_patient_saved(self, patient_id: int):
        """Handle patient saved event"""
        self.refresh_data()
        self.status_label.setText(f"Patient saved successfully (ID: {patient_id})")
    
    def refresh_data(self):
        """Refresh all patient data"""
        self.table_widget.load_patients()
        
        if self.current_view == "cards":
            # Update card view
            if hasattr(self.table_widget, 'filtered_patients'):
                self.card_widget.set_patients(self.table_widget.filtered_patients)
    
    def export_patients(self, format_type: str):
        """Export all patients in specified format"""
        file_filters = {
            'csv': "CSV Files (*.csv)",
            'json': "JSON Files (*.json)",
            'xlsx': "Excel Files (*.xlsx)",
            'pdf': "PDF Files (*.pdf)"
        }
        
        default_filename = f"patients_export.{format_type}"
        filename, _ = QFileDialog.getSaveFileName(
            self, f"Export Patients as {format_type.upper()}", 
            default_filename, file_filters.get(format_type, "All Files (*)")
        )
        
        if filename:
            try:
                patients = self.table_widget.filtered_patients if hasattr(self.table_widget, 'filtered_patients') else []
                
                if not patients:
                    QMessageBox.warning(self, "No Data", "No patients to export.")
                    return
                
                success = self.exporter.export_patients(patients, filename, format_type)
                
                if success:
                    QMessageBox.information(
                        self, "Export Successful", 
                        f"Successfully exported {len(patients)} patients to {filename}"
                    )
                    self.status_label.setText(f"Exported {len(patients)} patients to {format_type.upper()}")
                else:
                    QMessageBox.critical(self, "Export Failed", "Failed to export patients.")
                    
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Error exporting patients:\n{str(e)}")
    
    def export_selected_patients(self):
        """Export selected patients"""
        if self.current_view != "table":
            QMessageBox.information(self, "Info", "Please switch to table view to select patients for export.")
            return
        
        selected_ids = self.table_widget.get_selected_patient_ids()
        
        if not selected_ids:
            QMessageBox.warning(self, "No Selection", "Please select patients to export.")
            return
        
        # Show format selection dialog
        format_dialog = QMessageBox(self)
        format_dialog.setWindowTitle("Export Format")
        format_dialog.setText("Choose export format:")
        
        csv_btn = format_dialog.addButton("CSV", QMessageBox.ButtonRole.ActionRole)
        json_btn = format_dialog.addButton("JSON", QMessageBox.ButtonRole.ActionRole)
        
        if 'xlsx' in self.exporter.get_supported_formats():
            excel_btn = format_dialog.addButton("Excel", QMessageBox.ButtonRole.ActionRole)
        
        cancel_btn = format_dialog.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        
        format_dialog.exec()
        clicked_button = format_dialog.clickedButton()
        
        if clicked_button == cancel_btn:
            return
        
        # Determine format
        if clicked_button == csv_btn:
            format_type = 'csv'
        elif clicked_button == json_btn:
            format_type = 'json'
        elif 'xlsx' in self.exporter.get_supported_formats() and clicked_button == excel_btn:
            format_type = 'xlsx'
        else:
            return
        
        # Get filename
        file_filters = {
            'csv': "CSV Files (*.csv)",
            'json': "JSON Files (*.json)",
            'xlsx': "Excel Files (*.xlsx)"
        }
        
        filename, _ = QFileDialog.getSaveFileName(
            self, f"Export Selected Patients", 
            f"selected_patients.{format_type}", 
            file_filters[format_type]
        )
        
        if filename:
            try:
                # Get selected patients data
                selected_patients = [p for p in self.table_widget.filtered_patients if p.id in selected_ids]
                
                success = self.exporter.export_patients(selected_patients, filename, format_type)
                
                if success:
                    QMessageBox.information(
                        self, "Export Successful", 
                        f"Successfully exported {len(selected_patients)} selected patients"
                    )
                else:
                    QMessageBox.critical(self, "Export Failed", "Failed to export selected patients.")
                    
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Error exporting patients:\n{str(e)}")
    
    def import_patients(self, format_type: str):
        """Import patients from file"""
        file_filters = {
            'csv': "CSV Files (*.csv)",
            'json': "JSON Files (*.json)",
            'xlsx': "Excel Files (*.xlsx)"
        }
        
        filename, _ = QFileDialog.getOpenFileName(
            self, f"Import Patients from {format_type.upper()}", 
            "", file_filters.get(format_type, "All Files (*)")
        )
        
        if filename:
            # Show preview dialog first
            preview_data, errors = self.importer.preview_import(filename, max_rows=5)
            
            if errors:
                QMessageBox.critical(self, "Import Error", f"Error reading file:\n{'; '.join(errors)}")
                return
            
            if not preview_data:
                QMessageBox.warning(self, "No Data", "No data found in the file.")
                return
            
            # Show preview and confirm
            preview_text = "Preview of data to be imported:\n\n"
            for i, row in enumerate(preview_data[:3]):
                preview_text += f"Row {i+1}: {str(row)}\n"
            
            if len(preview_data) > 3:
                preview_text += f"... and {len(preview_data) - 3} more rows"
            
            reply = QMessageBox.question(
                self, "Confirm Import",
                f"{preview_text}\n\nDo you want to proceed with the import?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.start_import(filename)
    
    def start_import(self, filename: str):
        """Start the import process"""
        # Create progress dialog
        self.progress_dialog = QProgressDialog("Importing patients...", "Cancel", 0, 100, self)
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.show()
        
        # Start import worker
        self.import_worker = ImportWorker(filename, self.importer)
        self.import_worker.progress_updated.connect(self.progress_dialog.setValue)
        self.import_worker.import_completed.connect(self.on_import_completed)
        self.progress_dialog.canceled.connect(self.import_worker.terminate)
        self.import_worker.start()
    
    @pyqtSlot(int, int, list)
    def on_import_completed(self, imported: int, errors: int, error_list: List[str]):
        """Handle import completion"""
        self.progress_dialog.close()
        
        if imported > 0:
            message = f"Successfully imported {imported} patients."
            if errors > 0:
                message += f"\n{errors} errors occurred."
            
            QMessageBox.information(self, "Import Completed", message)
            
            if error_list:
                # Show errors in a separate dialog
                error_dialog = QMessageBox(self)
                error_dialog.setWindowTitle("Import Errors")
                error_dialog.setText("The following errors occurred during import:")
                error_dialog.setDetailedText("\n".join(error_list))
                error_dialog.exec()
            
            self.refresh_data()
            self.status_label.setText(f"Imported {imported} patients")
        else:
            QMessageBox.critical(
                self, "Import Failed", 
                f"Import failed. {errors} errors occurred:\n" + "\n".join(error_list[:5])
            )
    
    def download_import_template(self):
        """Download a CSV template for importing patients"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Import Template", "patient_import_template.csv", "CSV Files (*.csv)"
        )
        
        if filename:
            try:
                import csv
                
                headers = [
                    'first_name', 'last_name', 'date_of_birth', 'age', 'gender',
                    'phone', 'email', 'address', 'city', 'state', 'zip_code',
                    'insurance_provider', 'emergency_contact_name', 'emergency_contact_phone',
                    'allergies', 'chronic_conditions'
                ]
                
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(headers)
                    
                    # Add sample data
                    sample_data = [
                        'John', 'Doe', '1980-01-15', '44', 'Male',
                        '(555) 123-4567', 'john.doe@email.com', '123 Main St', 'Anytown', 'CA', '12345',
                        'Blue Cross', 'Jane Doe', '(555) 987-6543',
                        'Penicillin allergy', 'Hypertension'
                    ]
                    writer.writerow(sample_data)
                
                QMessageBox.information(self, "Template Created", f"Import template saved to {filename}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create template:\n{str(e)}")
    
    def cleanup_duplicates(self):
        """Cleanup duplicate patient records"""
        QMessageBox.information(self, "Cleanup", "Duplicate cleanup functionality will be implemented")
    
    def backup_data(self):
        """Backup patient data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"patient_backup_{timestamp}.json"
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Backup Patient Data", default_filename, "JSON Files (*.json)"
        )
        
        if filename:
            self.export_patients('json')
    
    def generate_summary_report(self):
        """Generate patient summary report"""
        try:
            patients = self.table_widget.patients if hasattr(self.table_widget, 'patients') else []
            summary = self.exporter.create_summary_report(patients)
            
            # Create summary dialog
            dialog = QMessageBox(self)
            dialog.setWindowTitle("Patient Summary Report")
            
            summary_text = f"""
Patient Summary Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Total Patients: {summary['total_patients']}

Demographics:
- Male: {summary['demographics']['gender_distribution'].get('Male', 0)}
- Female: {summary['demographics']['gender_distribution'].get('Female', 0)}
- Other: {summary['demographics']['gender_distribution'].get('Other', 0)}

Age Distribution:
- 0-18: {summary['demographics']['age_distribution']['0-18']}
- 19-35: {summary['demographics']['age_distribution']['19-35']}
- 36-50: {summary['demographics']['age_distribution']['36-50']}
- 51-65: {summary['demographics']['age_distribution']['51-65']}
- 65+: {summary['demographics']['age_distribution']['65+']}

Insurance Status:
- Insured: {summary['insurance_status']['insured']} ({summary['insurance_status']['insurance_rate']}%)
- Uninsured: {summary['insurance_status']['uninsured']}

Medical Information:
- Patients with Allergies: {summary['medical_info']['patients_with_allergies']} ({summary['medical_info']['allergy_rate']}%)
- Patients with Chronic Conditions: {summary['medical_info']['patients_with_chronic_conditions']} ({summary['medical_info']['chronic_condition_rate']}%)
            """
            
            dialog.setText(summary_text)
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate summary report:\n{str(e)}")
    
    def generate_demographics_report(self):
        """Generate demographics report"""
        QMessageBox.information(self, "Demographics", "Demographics report functionality will be implemented")
    
    def open_settings(self):
        """Open patient management settings"""
        QMessageBox.information(self, "Settings", "Patient management settings will be implemented")
    
    def get_current_patients(self) -> List:
        """Get current list of patients"""
        if hasattr(self.table_widget, 'filtered_patients'):
            return self.table_widget.filtered_patients
        return []
    
    def refresh(self):
        """Refresh all data"""
        self.refresh_data()
