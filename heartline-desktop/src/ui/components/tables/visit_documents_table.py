"""
Visit Documents Table Widget for Heartline Desktop Application

This widget displays all visit documents in a table format with search and filtering capabilities.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QHeaderView, QLineEdit, QLabel, QMessageBox,
    QComboBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import List, Optional

from src.models.complete_models import VisitDocument
from src.core.database import db_manager
from src.ui.styles import AppColors, AppStyles

class VisitDocumentsTableWidget(QWidget):
    """Widget for displaying and managing visit documents table"""
    
    # Signals
    document_selected = pyqtSignal(int)  # Emitted when document is selected
    document_edit_requested = pyqtSignal(int)  # Emitted when edit is requested
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.documents: List[VisitDocument] = []
        self.setup_ui()
        self.setup_connections()
        self.load_documents()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Apply comprehensive styling to the whole widget
        self.setStyleSheet(AppStyles.APP_STYLE)
        
        # Title
        title_label = QLabel("📄 Visit Documents Management")
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
        self.search_input.setPlaceholderText("Search by patient name or notes...")
        filter_layout.addWidget(self.search_input)
        
        # Document type filter
        filter_layout.addWidget(QLabel("Type:"))
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All Types", "blood", "mri", "xray", "ecg", "other"])
        filter_layout.addWidget(self.type_filter)
        
        # Action buttons
        filter_layout.addStretch()
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.upload_document_btn = QPushButton("📤 Upload Document")
        self.view_document_btn = QPushButton("👁️ View")
        self.download_document_btn = QPushButton("💾 Download")
        self.delete_document_btn = QPushButton("🗑️ Delete")
        
        self.refresh_btn.setObjectName("primary-button")
        self.upload_document_btn.setObjectName("success-button")
        self.view_document_btn.setObjectName("primary-button")
        self.download_document_btn.setObjectName("primary-button")
        self.delete_document_btn.setObjectName("danger-button")
        
        filter_layout.addWidget(self.refresh_btn)
        filter_layout.addWidget(self.upload_document_btn)
        filter_layout.addWidget(self.view_document_btn)
        filter_layout.addWidget(self.download_document_btn)
        filter_layout.addWidget(self.delete_document_btn)
        
        layout.addWidget(filter_frame)
        
        # Documents table
        self.setup_table()
        layout.addWidget(self.documents_table)
        
        # Status bar
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #666; padding: 5px;")
        layout.addWidget(self.status_label)
    
    def setup_table(self):
        """Setup the documents table"""
        # Define columns
        self.columns = [
            ("ID", 60),
            ("Visit ID", 80),
            ("Patient", 150),
            ("Document Type", 120),
            ("File Name", 200),
            ("Notes", 200),
            ("Upload Date", 120)
        ]
        
        self.documents_table = QTableWidget()
        self.documents_table.setColumnCount(len(self.columns))
        
        # Set headers and column widths
        headers = []
        for i, (header, width) in enumerate(self.columns):
            headers.append(header)
            self.documents_table.setColumnWidth(i, width)
        
        self.documents_table.setHorizontalHeaderLabels(headers)
        
        # Table properties
        self.documents_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.documents_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.documents_table.setAlternatingRowColors(True)
        self.documents_table.setSortingEnabled(True)
        
        # Apply table styling
        self.documents_table.setStyleSheet(AppStyles.get_table_style())
        # Make table headers bold
        header = self.documents_table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.search_input.textChanged.connect(self.filter_documents)
        self.type_filter.currentTextChanged.connect(self.filter_documents)
        self.refresh_btn.clicked.connect(self.load_documents)
        self.upload_document_btn.clicked.connect(self.upload_document)
        self.view_document_btn.clicked.connect(self.view_selected_document)
        self.download_document_btn.clicked.connect(self.download_selected_document)
        self.delete_document_btn.clicked.connect(self.delete_selected_document)
        self.documents_table.itemSelectionChanged.connect(self.on_selection_changed)
        self.documents_table.itemDoubleClicked.connect(self.on_double_click)
    
    def load_documents(self):
        """Load all documents from database"""
        try:
            self.status_label.setText("Loading documents...")
            
            with db_manager.get_session() as session:
                documents = session.query(VisitDocument).join(VisitDocument.visit).order_by(VisitDocument.created_at.desc()).all()
                self.documents = documents
                self.populate_table(documents)
                
            self.status_label.setText(f"Loaded {len(documents)} documents")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load documents:\n{str(e)}")
            self.status_label.setText("Error loading documents")
    
    def populate_table(self, documents: List[VisitDocument]):
        """Populate table with document data"""
        self.documents_table.setRowCount(len(documents))
        
        for row, document in enumerate(documents):
            # ID
            self.documents_table.setItem(row, 0, QTableWidgetItem(str(document.id)))
            
            # Visit ID
            self.documents_table.setItem(row, 1, QTableWidgetItem(str(document.visit_id)))
            
            # Patient
            patient_name = f"{document.visit.patient.first_name} {document.visit.patient.last_name}" if document.visit and document.visit.patient else "N/A"
            self.documents_table.setItem(row, 2, QTableWidgetItem(patient_name))
            
            # Document Type
            doc_type = document.doc_type.upper() if document.doc_type else "N/A"
            self.documents_table.setItem(row, 3, QTableWidgetItem(doc_type))
            
            # File Name (extract from path)
            import os
            file_name = os.path.basename(document.file_path) if document.file_path else "N/A"
            self.documents_table.setItem(row, 4, QTableWidgetItem(file_name))
            
            # Notes
            notes = document.notes[:50] + "..." if document.notes and len(document.notes) > 50 else (document.notes or "No notes")
            self.documents_table.setItem(row, 5, QTableWidgetItem(notes))
            
            # Upload Date
            upload_date = document.created_at.strftime("%Y-%m-%d %H:%M") if document.created_at else "N/A"
            self.documents_table.setItem(row, 6, QTableWidgetItem(upload_date))
            
            # Store document ID in first column for reference
            self.documents_table.item(row, 0).setData(Qt.ItemDataRole.UserRole, document.id)
    
    def filter_documents(self):
        """Filter documents based on search criteria"""
        search_text = self.search_input.text().lower()
        type_filter = self.type_filter.currentText()
        
        filtered_documents = []
        
        for document in self.documents:
            # Text search
            if search_text:
                searchable_text = f"{document.notes or ''}"
                if document.visit and document.visit.patient:
                    searchable_text += f" {document.visit.patient.first_name} {document.visit.patient.last_name}"
                if search_text not in searchable_text.lower():
                    continue
            
            # Type filter
            if type_filter != "All Types" and document.doc_type != type_filter:
                continue
            
            filtered_documents.append(document)
        
        self.populate_table(filtered_documents)
        self.status_label.setText(f"Showing {len(filtered_documents)} of {len(self.documents)} documents")
    
    def on_selection_changed(self):
        """Handle selection change"""
        current_row = self.documents_table.currentRow()
        if current_row >= 0:
            item = self.documents_table.item(current_row, 0)
            if item:
                document_id = item.data(Qt.ItemDataRole.UserRole)
                if document_id:
                    self.document_selected.emit(document_id)
        
        # Enable/disable action buttons
        has_selection = current_row >= 0
        self.view_document_btn.setEnabled(has_selection)
        self.download_document_btn.setEnabled(has_selection)
        self.delete_document_btn.setEnabled(has_selection)
    
    def on_double_click(self, item):
        """Handle double click"""
        self.view_selected_document()
    
    def upload_document(self):
        """Upload new document"""
        # TODO: Open document upload dialog
        QMessageBox.information(self, "Upload Document", "Document upload dialog will be implemented here.")
    
    def view_selected_document(self):
        """View selected document"""
        current_row = self.documents_table.currentRow()
        if current_row >= 0:
            # TODO: Open document viewer
            QMessageBox.information(self, "View Document", "Document viewer will be implemented here.")
    
    def download_selected_document(self):
        """Download selected document"""
        current_row = self.documents_table.currentRow()
        if current_row >= 0:
            # TODO: Implement document download
            QMessageBox.information(self, "Download Document", "Document download will be implemented here.")
    
    def delete_selected_document(self):
        """Delete selected document"""
        current_row = self.documents_table.currentRow()
        if current_row >= 0:
            reply = QMessageBox.question(
                self, "Confirm Delete", 
                "Are you sure you want to delete this document?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # TODO: Implement document deletion
                QMessageBox.information(self, "Delete Document", "Document deletion will be implemented here.")
                self.load_documents()  # Refresh table
    
    def get_selected_document_id(self) -> Optional[int]:
        """Get the currently selected document ID"""
        current_row = self.documents_table.currentRow()
        if current_row >= 0:
            item = self.documents_table.item(current_row, 0)
            if item:
                return item.data(Qt.ItemDataRole.UserRole)
        return None
