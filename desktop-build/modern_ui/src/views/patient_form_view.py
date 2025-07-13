"""
Patient Form View for HeartLine Desktop Application
Modern patient registration form with validation and beautiful UI
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import re

class PatientFormView(ctk.CTkScrollableFrame):
    """
    Modern patient registration form matching the Flask app design
    """
    
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.app = app
        self.form_data = {}
        self.setup_form()
    
    def setup_form(self):
        """Create the complete patient form layout"""
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        
        # Form header
        self.create_form_header()
        
        # Main form card
        self.create_form_card()
    
    def create_form_header(self):
        """Create the form header with instructions"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="👤 Create New Patient",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.app.colors['text_dark']
        )
        title_label.pack(anchor="w")
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Enter patient information to create a new medical record",
            font=ctk.CTkFont(size=14),
            text_color=self.app.colors['text_light']
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))
    
    def create_form_card(self):
        """Create the main form card"""
        form_card = ctk.CTkFrame(
            self,
            corner_radius=15,
            fg_color=self.app.colors['white']
        )
        form_card.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Form content
        form_content = ctk.CTkFrame(form_card, fg_color="transparent")
        form_content.pack(fill="both", expand=True, padx=30, pady=30)
        form_content.grid_columnconfigure((0, 1), weight=1)
        
        # Personal Information Section
        self.create_personal_info_section(form_content)
        
        # Contact Information Section
        self.create_contact_info_section(form_content)
        
        # Medical Information Section
        self.create_medical_info_section(form_content)
        
        # Emergency Contact Section
        self.create_emergency_contact_section(form_content)
        
        # Form buttons
        self.create_form_buttons(form_content)
    
    def create_section_header(self, parent, title, icon, row):
        """Create a section header"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(20, 10))
        
        # Section title with icon
        title_label = ctk.CTkLabel(
            header_frame,
            text=f"{icon} {title}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.app.colors['primary']
        )
        title_label.pack(side="left")
        
        # Separator line
        separator = ctk.CTkFrame(header_frame, height=2, fg_color=self.app.colors['background'])
        separator.pack(fill="x", padx=(20, 0), pady=10)
        
        return row + 1
    
    def create_form_field(self, parent, label_text, row, column=0, columnspan=1, field_type="entry", options=None, required=True):
        """Create a form field with label and input"""
        # Field frame
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.grid(row=row, column=column, columnspan=columnspan, sticky="ew", padx=10, pady=5)
        field_frame.grid_columnconfigure(0, weight=1)
        
        # Label with required indicator
        label_text_full = f"{label_text} {'*' if required else ''}"
        label = ctk.CTkLabel(
            field_frame,
            text=label_text_full,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.app.colors['text_dark']
        )
        label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        # Input field based on type
        if field_type == "entry":
            widget = ctk.CTkEntry(
                field_frame,
                height=40,
                corner_radius=8,
                font=ctk.CTkFont(size=12)
            )
        elif field_type == "combobox":
            widget = ctk.CTkComboBox(
                field_frame,
                values=options or [],
                height=40,
                corner_radius=8,
                font=ctk.CTkFont(size=12)
            )
        elif field_type == "textbox":
            widget = ctk.CTkTextbox(
                field_frame,
                height=80,
                corner_radius=8,
                font=ctk.CTkFont(size=12)
            )
        elif field_type == "date":
            widget = ctk.CTkEntry(
                field_frame,
                height=40,
                corner_radius=8,
                font=ctk.CTkFont(size=12),
                placeholder_text="YYYY-MM-DD"
            )
        
        widget.grid(row=1, column=0, sticky="ew")
        
        return widget
    
    def create_personal_info_section(self, parent):
        """Create personal information section"""
        row = self.create_section_header(parent, "Personal Information", "👤", 0)
        
        # First Name and Last Name
        self.first_name_entry = self.create_form_field(parent, "First Name", row, 0)
        self.last_name_entry = self.create_form_field(parent, "Last Name", row, 1)
        row += 1
        
        # Date of Birth and Gender
        self.dob_entry = self.create_form_field(parent, "Date of Birth", row, 0, field_type="date")
        self.gender_combo = self.create_form_field(
            parent, "Gender", row, 1, 
            field_type="combobox", 
            options=["Male", "Female", "Other", "Prefer not to say"]
        )
        row += 1
        
        # ID Number and Nationality
        self.id_number_entry = self.create_form_field(parent, "ID Number", row, 0, required=False)
        self.nationality_entry = self.create_form_field(parent, "Nationality", row, 1, required=False)
        
        return row + 1
    
    def create_contact_info_section(self, parent):
        """Create contact information section"""
        row = self.create_section_header(parent, "Contact Information", "📞", 4)
        
        # Phone and Email
        self.phone_entry = self.create_form_field(parent, "Phone Number", row, 0)
        self.email_entry = self.create_form_field(parent, "Email Address", row, 1, required=False)
        row += 1
        
        # Address
        self.address_textbox = self.create_form_field(
            parent, "Address", row, 0, columnspan=2, field_type="textbox"
        )
        
        return row + 1
    
    def create_medical_info_section(self, parent):
        """Create medical information section"""
        row = self.create_section_header(parent, "Medical Information", "🏥", 7)
        
        # Blood Type and Insurance
        self.blood_type_combo = self.create_form_field(
            parent, "Blood Type", row, 0,
            field_type="combobox",
            options=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"],
            required=False
        )
        self.insurance_entry = self.create_form_field(parent, "Insurance Provider", row, 1, required=False)
        row += 1
        
        # Allergies
        self.allergies_textbox = self.create_form_field(
            parent, "Known Allergies", row, 0, columnspan=2, 
            field_type="textbox", required=False
        )
        row += 1
        
        # Medical History
        self.medical_history_textbox = self.create_form_field(
            parent, "Medical History", row, 0, columnspan=2, 
            field_type="textbox", required=False
        )
        
        return row + 1
    
    def create_emergency_contact_section(self, parent):
        """Create emergency contact section"""
        row = self.create_section_header(parent, "Emergency Contact", "🚨", 11)
        
        # Emergency Contact Name and Relationship
        self.emergency_name_entry = self.create_form_field(parent, "Contact Name", row, 0, required=False)
        self.emergency_relationship_entry = self.create_form_field(parent, "Relationship", row, 1, required=False)
        row += 1
        
        # Emergency Contact Phone
        self.emergency_phone_entry = self.create_form_field(parent, "Contact Phone", row, 0, required=False)
        
        return row + 1
    
    def create_form_buttons(self, parent):
        """Create form action buttons"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.grid(row=15, column=0, columnspan=2, pady=(30, 0))
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=120,
            height=45,
            corner_radius=8,
            fg_color="transparent",
            border_width=2,
            border_color=self.app.colors['text_light'],
            text_color=self.app.colors['text_light'],
            hover_color=self.app.colors['background'],
            command=self.cancel_form
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        # Save button
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Save Patient",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            height=45,
            corner_radius=8,
            fg_color=self.app.colors['primary'],
            hover_color=self.app.colors['primary_dark'],
            command=self.save_patient
        )
        save_btn.pack(side="right")
        
        # Clear form button
        clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Clear Form",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=130,
            height=45,
            corner_radius=8,
            fg_color=self.app.colors['warning'],
            hover_color="#e0a800",
            command=self.clear_form
        )
        clear_btn.pack(side="right", padx=(0, 10))
    
    def validate_form(self):
        """Validate form data"""
        errors = []
        
        # Required fields
        if not self.first_name_entry.get().strip():
            errors.append("First name is required")
        
        if not self.last_name_entry.get().strip():
            errors.append("Last name is required")
        
        if not self.phone_entry.get().strip():
            errors.append("Phone number is required")
        
        # Date validation
        dob_text = self.dob_entry.get().strip()
        if dob_text:
            try:
                dob = datetime.strptime(dob_text, "%Y-%m-%d").date()
                if dob >= date.today():
                    errors.append("Date of birth must be in the past")
            except ValueError:
                errors.append("Date of birth must be in YYYY-MM-DD format")
        else:
            errors.append("Date of birth is required")
        
        # Email validation (if provided)
        email_text = self.email_entry.get().strip()
        if email_text:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email_text):
                errors.append("Please enter a valid email address")
        
        # Phone validation
        phone_text = self.phone_entry.get().strip()
        if phone_text:
            # Remove common phone formatting
            phone_clean = re.sub(r'[^0-9+]', '', phone_text)
            if len(phone_clean) < 10:
                errors.append("Please enter a valid phone number")
        
        return errors
    
    def save_patient(self):
        """Save patient data"""
        # Validate form
        errors = self.validate_form()
        if errors:
            error_message = "Please correct the following errors:\\n\\n" + "\\n".join(f"• {error}" for error in errors)
            messagebox.showerror("Validation Error", error_message)
            return
        
        # Collect form data
        patient_data = {
            'first_name': self.first_name_entry.get().strip(),
            'last_name': self.last_name_entry.get().strip(),
            'date_of_birth': self.dob_entry.get().strip(),
            'gender': self.gender_combo.get(),
            'id_number': self.id_number_entry.get().strip(),
            'nationality': self.nationality_entry.get().strip(),
            'phone': self.phone_entry.get().strip(),
            'email': self.email_entry.get().strip(),
            'address': self.address_textbox.get("1.0", "end-1c").strip(),
            'blood_type': self.blood_type_combo.get(),
            'insurance': self.insurance_entry.get().strip(),
            'allergies': self.allergies_textbox.get("1.0", "end-1c").strip(),
            'medical_history': self.medical_history_textbox.get("1.0", "end-1c").strip(),
            'emergency_contact_name': self.emergency_name_entry.get().strip(),
            'emergency_relationship': self.emergency_relationship_entry.get().strip(),
            'emergency_phone': self.emergency_phone_entry.get().strip()
        }
        
        # Here you would save to database
        # For now, just show success message
        success_message = f"Patient {patient_data['first_name']} {patient_data['last_name']} has been successfully registered!"
        messagebox.showinfo("Success", success_message)
        
        # Clear form and navigate to patients list
        self.clear_form()
        self.app.show_patients()
    
    def clear_form(self):
        """Clear all form fields"""
        # Entry fields
        for entry in [self.first_name_entry, self.last_name_entry, self.dob_entry, 
                     self.id_number_entry, self.nationality_entry, self.phone_entry, 
                     self.email_entry, self.insurance_entry, self.emergency_name_entry,
                     self.emergency_relationship_entry, self.emergency_phone_entry]:
            entry.delete(0, 'end')
        
        # Combo boxes
        self.gender_combo.set("")
        self.blood_type_combo.set("")
        
        # Text boxes
        self.address_textbox.delete("1.0", "end")
        self.allergies_textbox.delete("1.0", "end")
        self.medical_history_textbox.delete("1.0", "end")
    
    def cancel_form(self):
        """Cancel form and return to dashboard"""
        if messagebox.askyesno("Cancel", "Are you sure you want to cancel? All entered data will be lost."):
            self.app.show_dashboard()
