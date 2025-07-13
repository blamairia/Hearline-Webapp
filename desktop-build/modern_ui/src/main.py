"""
HeartLine Medical Clinic - Modern Desktop Application
A beautiful, responsive, and feature-rich desktop version of the HeartLine web application

Built with CustomTkinter for modern UI/UX that matches the original Flask app design
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any, Callable
import threading
import time
from datetime import datetime, date

# Configure CustomTkinter appearance
ctk.set_appearance_mode("light")  # Can be "light", "dark", or "system"
ctk.set_default_color_theme("blue")  # Can be "blue", "green", or "dark-blue"

class HeartLineDesktopApp:
    """
    Main HeartLine Desktop Application
    Replicates the Flask app's UI with modern desktop components
    """
    
    def __init__(self):
        # Application configuration
        self.app_title = "HeartLine Medical Clinic"
        self.app_version = "Desktop v1.0"
        self.current_user = None
        self.current_view = None
        
        # Color scheme matching the Flask app
        self.colors = {
            'primary': '#0074d9',          # Main blue
            'primary_dark': '#0056b3',     # Darker blue
            'secondary': '#00b4ff',        # Light blue
            'accent': '#667eea',           # Purple accent
            'success': '#28a745',          # Green
            'warning': '#ffc107',          # Yellow
            'danger': '#dc3545',           # Red
            'background': '#f8f9fa',       # Light gray background
            'sidebar': '#0074d9',          # Sidebar blue
            'white': '#ffffff',
            'text_dark': '#212529',
            'text_light': '#6c757d'
        }
        
        # Initialize the main window
        self.setup_main_window()
        
        # Initialize components
        self.setup_sidebar()
        self.setup_main_content_area()
        self.setup_status_bar()
        
        # Load initial view
        self.show_dashboard()
        
    def setup_main_window(self):
        """Initialize the main application window with modern styling"""
        self.root = ctk.CTk()
        self.root.title(self.app_title)
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        
        # Center window on screen
        self.center_window()
        
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Set window icon (if available)
        try:
            icon_path = Path(__file__).parent.parent.parent / "static" / "img" / "HeartLine.png"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except:
            pass
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_sidebar(self):
        """Create the modern sidebar navigation matching the Flask app"""
        # Sidebar frame
        self.sidebar = ctk.CTkFrame(
            self.root,
            width=250,
            corner_radius=0,
            fg_color=self.colors['primary']
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar.grid_propagate(False)
        
        # Sidebar header with logo and title
        self.setup_sidebar_header()
        
        # Navigation menu
        self.setup_navigation_menu()
        
        # Sidebar footer
        self.setup_sidebar_footer()
    
    def setup_sidebar_header(self):
        """Create the sidebar header with logo and branding"""
        # Header frame
        header_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent",
            height=120
        )
        header_frame.pack(fill="x", padx=15, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        # Logo placeholder (will add actual logo later)
        logo_frame = ctk.CTkFrame(
            header_frame,
            width=80,
            height=80,
            corner_radius=40,
            fg_color=self.colors['white']
        )
        logo_frame.pack(pady=(10, 5))
        
        # Logo text (placeholder)
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="❤️",
            font=ctk.CTkFont(size=30),
            text_color=self.colors['primary']
        )
        logo_label.pack(expand=True)
        
        # App title
        title_label = ctk.CTkLabel(
            header_frame,
            text="HeartLine",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors['white']
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Medical Clinic",
            font=ctk.CTkFont(size=12),
            text_color=self.colors['white']
        )
        subtitle_label.pack()
    
    def setup_navigation_menu(self):
        """Create the navigation menu with modern buttons"""
        # Navigation frame
        nav_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        nav_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Navigation items matching the Flask app
        self.nav_items = [
            {"text": "Dashboard", "icon": "🏠", "command": self.show_dashboard, "active": True},
            {"text": "New Patient", "icon": "👤", "command": self.show_new_patient, "active": False},
            {"text": "New Visit", "icon": "📋", "command": self.show_new_visit, "active": False},
            {"text": "Patients", "icon": "👥", "command": self.show_patients, "active": False},
            {"text": "Visits", "icon": "📊", "command": self.show_visits, "active": False},
            {"text": "Appointments", "icon": "📅", "command": self.show_appointments, "active": False},
            {"text": "ECG History", "icon": "💓", "command": self.show_ecg_history, "active": False},
        ]
        
        self.nav_buttons = []
        
        for item in self.nav_items:
            btn = self.create_nav_button(nav_frame, item)
            self.nav_buttons.append(btn)
    
    def create_nav_button(self, parent, item: Dict[str, Any]) -> ctk.CTkButton:
        """Create a navigation button with hover effects"""
        button = ctk.CTkButton(
            parent,
            text=f"{item['icon']}  {item['text']}",
            font=ctk.CTkFont(size=14, weight="normal"),
            height=45,
            corner_radius=8,
            fg_color="transparent" if not item['active'] else self.colors['white'],
            text_color=self.colors['white'] if not item['active'] else self.colors['primary'],
            hover_color=("gray75", "gray25"),
            anchor="w",
            command=lambda cmd=item['command']: self.handle_nav_click(cmd)
        )
        button.pack(fill="x", pady=2)
        
        return button
    
    def handle_nav_click(self, command: Callable):
        """Handle navigation button clicks"""
        # Reset all buttons to inactive state
        for i, button in enumerate(self.nav_buttons):
            button.configure(
                fg_color="transparent",
                text_color=self.colors['white']
            )
            self.nav_items[i]['active'] = False
        
        # Execute the command
        command()
    
    def set_active_nav_button(self, index: int):
        """Set a navigation button as active"""
        if 0 <= index < len(self.nav_buttons):
            self.nav_buttons[index].configure(
                fg_color=self.colors['white'],
                text_color=self.colors['primary']
            )
            self.nav_items[index]['active'] = True
    
    def setup_sidebar_footer(self):
        """Create the sidebar footer with user info and settings"""
        footer_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent",
            height=80
        )
        footer_frame.pack(fill="x", side="bottom", padx=10, pady=10)
        footer_frame.pack_propagate(False)
        
        # User info (placeholder)
        user_frame = ctk.CTkFrame(
            footer_frame,
            fg_color=self.colors['primary_dark'],
            corner_radius=8
        )
        user_frame.pack(fill="x", pady=5)
        
        user_label = ctk.CTkLabel(
            user_frame,
            text="👨‍⚕️ Dr. Admin",
            font=ctk.CTkFont(size=12),
            text_color=self.colors['white']
        )
        user_label.pack(pady=8)
        
        # Settings button
        settings_btn = ctk.CTkButton(
            footer_frame,
            text="⚙️  Settings",
            font=ctk.CTkFont(size=12),
            height=30,
            fg_color="transparent",
            text_color=self.colors['white'],
            hover_color=("gray75", "gray25"),
            command=self.show_settings
        )
        settings_btn.pack(fill="x")
    
    def setup_main_content_area(self):
        """Create the main content area where views will be displayed"""
        # Main content frame
        self.main_frame = ctk.CTkFrame(
            self.root,
            corner_radius=0,
            fg_color=self.colors['background']
        )
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Top bar with breadcrumbs and actions
        self.setup_top_bar()
        
        # Content container
        self.content_container = ctk.CTkFrame(
            self.main_frame,
            corner_radius=0,
            fg_color="transparent"
        )
        self.content_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)
    
    def setup_top_bar(self):
        """Create the top navigation bar"""
        top_bar = ctk.CTkFrame(
            self.main_frame,
            height=60,
            corner_radius=0,
            fg_color=self.colors['white']
        )
        top_bar.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 1))
        top_bar.grid_propagate(False)
        top_bar.grid_columnconfigure(1, weight=1)
        
        # Current view title
        self.page_title = ctk.CTkLabel(
            top_bar,
            text="Dashboard",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors['text_dark']
        )
        self.page_title.grid(row=0, column=0, sticky="w", padx=20, pady=15)
        
        # Action buttons
        action_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        action_frame.grid(row=0, column=2, sticky="e", padx=20, pady=10)
        
        # Quick action buttons
        new_patient_btn = ctk.CTkButton(
            action_frame,
            text="+ New Patient",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=35,
            fg_color=self.colors['primary'],
            hover_color=self.colors['primary_dark'],
            command=self.show_new_patient
        )
        new_patient_btn.pack(side="right", padx=(5, 0))
        
        new_visit_btn = ctk.CTkButton(
            action_frame,
            text="+ New Visit",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=35,
            fg_color=self.colors['success'],
            hover_color="#218838",
            command=self.show_new_visit
        )
        new_visit_btn.pack(side="right", padx=(5, 0))
    
    def setup_status_bar(self):
        """Create the bottom status bar"""
        self.status_bar = ctk.CTkFrame(
            self.root,
            height=25,
            corner_radius=0,
            fg_color=self.colors['text_light']
        )
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.status_bar.grid_propagate(False)
        
        # Status text
        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="Ready | Desktop Application v1.0",
            font=ctk.CTkFont(size=10),
            text_color=self.colors['white']
        )
        self.status_label.pack(side="left", padx=10, pady=2)
        
        # Current time
        self.time_label = ctk.CTkLabel(
            self.status_bar,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=self.colors['white']
        )
        self.time_label.pack(side="right", padx=10, pady=2)
        
        # Update time every second
        self.update_time()
    
    def update_time(self):
        """Update the time display in the status bar"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.configure(text=current_time)
        self.root.after(1000, self.update_time)
    
    def clear_content(self):
        """Clear the current content area"""
        for widget in self.content_container.winfo_children():
            widget.destroy()
    
    def set_page_title(self, title: str):
        """Update the page title"""
        self.page_title.configure(text=title)
    
    # Navigation methods - simplified without separate view classes for now
    def show_dashboard(self):
        """Display the dashboard view"""
        self.clear_content()
        self.set_page_title("📊 Dashboard")
        self.set_active_nav_button(0)
        
        # Create dashboard content directly
        self.create_dashboard_content()
    
    def show_new_patient(self):
        """Display the new patient form"""
        self.clear_content()
        self.set_page_title("👤 New Patient")
        self.set_active_nav_button(1)
        
        self.create_patient_form_content()
    
    def show_new_visit(self):
        """Display the new visit form"""
        self.clear_content()
        self.set_page_title("📋 New Visit")
        self.set_active_nav_button(2)
        
        self.create_visit_form_content()
    
    def show_patients(self):
        """Display the patients table"""
        self.clear_content()
        self.set_page_title("👥 Patients")
        self.set_active_nav_button(3)
        
        self.create_patients_table_content()
    
    def show_visits(self):
        """Display the visits table"""
        self.clear_content()
        self.set_page_title("📊 Visits")
        self.set_active_nav_button(4)
        
        self.create_visits_table_content()
    
    def show_appointments(self):
        """Display the appointments table"""
        self.clear_content()
        self.set_page_title("📅 Appointments")
        self.set_active_nav_button(5)
        
        self.create_appointments_table_content()
    
    def show_ecg_history(self):
        """Display the ECG history"""
        self.clear_content()
        self.set_page_title("💓 ECG History")
        self.set_active_nav_button(6)
        
        self.create_ecg_history_content()
    
    def show_settings(self):
        """Display the settings view"""
        self.clear_content()
        self.set_page_title("⚙️ Settings")
        
        self.create_settings_content()
    
    def run(self):
        """Start the application"""
        print("🚀 Starting HeartLine Desktop Application...")
        print(f"📱 UI Framework: CustomTkinter")
        print(f"🎨 Theme: Modern Medical Design")
        print(f"✨ Features: Responsive, Animated, Professional")
        self.root.mainloop()

    # Content creation methods
    def create_dashboard_content(self):
        """Create the dashboard content with statistics and recent activity"""
        # Main dashboard container
        dashboard_frame = ctk.CTkScrollableFrame(
            self.content_container,
            fg_color="transparent"
        )
        dashboard_frame.pack(fill="both", expand=True)
        
        # Welcome header
        welcome_frame = ctk.CTkFrame(
            dashboard_frame,
            fg_color=self.colors['white'],
            corner_radius=15
        )
        welcome_frame.pack(fill="x", pady=(0, 20))
        
        welcome_label = ctk.CTkLabel(
            welcome_frame,
            text="Welcome to HeartLine Medical Clinic",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.colors['primary']
        )
        welcome_label.pack(pady=20)
        
        # Statistics cards
        stats_frame = ctk.CTkFrame(dashboard_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Sample statistics
        stats = [
            {"title": "Total Patients", "value": "1,234", "icon": "👥", "color": self.colors['primary']},
            {"title": "Today's Visits", "value": "23", "icon": "📋", "color": self.colors['success']},
            {"title": "Appointments", "value": "45", "icon": "📅", "color": self.colors['warning']},
            {"title": "ECG Records", "value": "567", "icon": "💓", "color": self.colors['danger']},
        ]
        
        for i, stat in enumerate(stats):
            self.create_stat_card(stats_frame, stat, i)
        
        # Recent activity section
        activity_frame = ctk.CTkFrame(
            dashboard_frame,
            fg_color=self.colors['white'],
            corner_radius=15
        )
        activity_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        activity_header = ctk.CTkLabel(
            activity_frame,
            text="📊 Recent Activity",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors['text_dark']
        )
        activity_header.pack(pady=(20, 10))
        
        # Sample recent activities
        activities = [
            "New patient registered: John Doe",
            "ECG analysis completed for Patient #1234",
            "Appointment scheduled for tomorrow",
            "Visit documented for Jane Smith",
            "Prescription updated for Patient #5678"
        ]
        
        for activity in activities:
            activity_item = ctk.CTkLabel(
                activity_frame,
                text=f"• {activity}",
                font=ctk.CTkFont(size=14),
                text_color=self.colors['text_light'],
                anchor="w"
            )
            activity_item.pack(fill="x", padx=20, pady=2)
    
    def create_stat_card(self, parent, stat, column):
        """Create a statistics card"""
        card = ctk.CTkFrame(
            parent,
            fg_color=stat['color'],
            corner_radius=15,
            height=120
        )
        card.grid(row=0, column=column, padx=10, pady=10, sticky="ew")
        card.grid_propagate(False)
        
        # Icon
        icon_label = ctk.CTkLabel(
            card,
            text=stat['icon'],
            font=ctk.CTkFont(size=30),
            text_color=self.colors['white']
        )
        icon_label.pack(pady=(15, 5))
        
        # Value
        value_label = ctk.CTkLabel(
            card,
            text=stat['value'],
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors['white']
        )
        value_label.pack()
        
        # Title
        title_label = ctk.CTkLabel(
            card,
            text=stat['title'],
            font=ctk.CTkFont(size=12),
            text_color=self.colors['white']
        )
        title_label.pack(pady=(0, 15))
    
    def create_patient_form_content(self):
        """Create the new patient form"""
        form_frame = ctk.CTkScrollableFrame(
            self.content_container,
            fg_color=self.colors['white'],
            corner_radius=15
        )
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Form header
        header_label = ctk.CTkLabel(
            form_frame,
            text="👤 Patient Information",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors['primary']
        )
        header_label.pack(pady=(20, 30))
        
        # Form fields
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(fill="x", padx=40, pady=20)
        
        # Name fields
        name_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=10)
        name_frame.grid_columnconfigure((0, 1), weight=1)
        
        # First name
        ctk.CTkLabel(name_frame, text="First Name", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=(0, 10))
        first_name_entry = ctk.CTkEntry(name_frame, placeholder_text="Enter first name", height=40)
        first_name_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(5, 0))
        
        # Last name
        ctk.CTkLabel(name_frame, text="Last Name", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, sticky="w")
        last_name_entry = ctk.CTkEntry(name_frame, placeholder_text="Enter last name", height=40)
        last_name_entry.grid(row=1, column=1, sticky="ew", pady=(5, 0))
        
        # Personal info
        personal_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        personal_frame.pack(fill="x", pady=10)
        personal_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Date of birth
        ctk.CTkLabel(personal_frame, text="Date of Birth", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=(0, 10))
        dob_entry = ctk.CTkEntry(personal_frame, placeholder_text="YYYY-MM-DD", height=40)
        dob_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(5, 0))
        
        # Gender
        ctk.CTkLabel(personal_frame, text="Gender", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, sticky="w", padx=(0, 10))
        gender_combo = ctk.CTkComboBox(personal_frame, values=["Male", "Female", "Other"], height=40)
        gender_combo.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(5, 0))
        
        # Phone
        ctk.CTkLabel(personal_frame, text="Phone Number", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, sticky="w")
        phone_entry = ctk.CTkEntry(personal_frame, placeholder_text="Enter phone number", height=40)
        phone_entry.grid(row=1, column=2, sticky="ew", pady=(5, 0))
        
        # Email
        email_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        email_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(email_frame, text="Email Address", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        email_entry = ctk.CTkEntry(email_frame, placeholder_text="Enter email address", height=40)
        email_entry.pack(fill="x", pady=(5, 0))
        
        # Address
        address_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        address_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(address_frame, text="Address", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        address_text = ctk.CTkTextbox(address_frame, height=80)
        address_text.pack(fill="x", pady=(5, 0))
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=40, pady=30)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Save Patient",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            fg_color=self.colors['success'],
            hover_color="#218838",
            command=self.save_patient
        )
        save_btn.pack(side="right", padx=(10, 0))
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="❌ Cancel",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            fg_color=self.colors['text_light'],
            hover_color="#5a6268",
            command=self.show_dashboard
        )
        cancel_btn.pack(side="right")
    
    def create_visit_form_content(self):
        """Create the new visit form"""
        placeholder_frame = self.create_placeholder_content("📋 Visit Form", "Create a new patient visit with ECG analysis")
    
    def create_patients_table_content(self):
        """Create the patients table view"""
        placeholder_frame = self.create_placeholder_content("👥 Patients Table", "View and manage all patients")
    
    def create_visits_table_content(self):
        """Create the visits table view"""
        placeholder_frame = self.create_placeholder_content("📊 Visits Table", "View all patient visits and records")
    
    def create_appointments_table_content(self):
        """Create the appointments table view"""
        placeholder_frame = self.create_placeholder_content("📅 Appointments", "Manage patient appointments and scheduling")
    
    def create_ecg_history_content(self):
        """Create the ECG history view"""
        placeholder_frame = self.create_placeholder_content("💓 ECG History", "View ECG analysis results and waveforms")
    
    def create_settings_content(self):
        """Create the settings view"""
        settings_frame = ctk.CTkScrollableFrame(
            self.content_container,
            fg_color=self.colors['white'],
            corner_radius=15
        )
        settings_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Settings header
        header_label = ctk.CTkLabel(
            settings_frame,
            text="⚙️ Application Settings",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors['primary']
        )
        header_label.pack(pady=(20, 30))
        
        # Theme settings
        theme_frame = ctk.CTkFrame(settings_frame, fg_color=self.colors['background'], corner_radius=10)
        theme_frame.pack(fill="x", padx=40, pady=10)
        
        theme_label = ctk.CTkLabel(theme_frame, text="🎨 Appearance", font=ctk.CTkFont(size=18, weight="bold"))
        theme_label.pack(pady=(15, 10))
        
        theme_switch = ctk.CTkSwitch(theme_frame, text="Dark Mode", command=self.toggle_theme)
        theme_switch.pack(pady=(0, 15))
        
        # Database settings
        db_frame = ctk.CTkFrame(settings_frame, fg_color=self.colors['background'], corner_radius=10)
        db_frame.pack(fill="x", padx=40, pady=10)
        
        db_label = ctk.CTkLabel(db_frame, text="🗄️ Database", font=ctk.CTkFont(size=18, weight="bold"))
        db_label.pack(pady=(15, 10))
        
        status_label = ctk.CTkLabel(db_frame, text="Status: Connected ✅", text_color=self.colors['success'])
        status_label.pack(pady=(0, 15))
    
    def create_placeholder_content(self, title: str, description: str):
        """Create placeholder content for views not yet implemented"""
        placeholder_frame = ctk.CTkFrame(
            self.content_container,
            fg_color=self.colors['white'],
            corner_radius=15
        )
        placeholder_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Center content
        center_frame = ctk.CTkFrame(placeholder_frame, fg_color="transparent")
        center_frame.pack(expand=True)
        
        title_label = ctk.CTkLabel(
            center_frame,
            text=title,
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=self.colors['primary']
        )
        title_label.pack(pady=(50, 20))
        
        desc_label = ctk.CTkLabel(
            center_frame,
            text=description,
            font=ctk.CTkFont(size=16),
            text_color=self.colors['text_light']
        )
        desc_label.pack()
        
        coming_soon_label = ctk.CTkLabel(
            center_frame,
            text="🚧 Coming Soon in Next Update",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors['warning']
        )
        coming_soon_label.pack(pady=(30, 50))
        
        return placeholder_frame
    
    # Event handlers
    def save_patient(self):
        """Handle patient save action"""
        # Show success message
        success_window = ctk.CTkToplevel(self.root)
        success_window.title("Success")
        success_window.geometry("300x150")
        success_window.transient(self.root)
        
        success_label = ctk.CTkLabel(
            success_window,
            text="✅ Patient saved successfully!",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        success_label.pack(expand=True)
        
        ok_btn = ctk.CTkButton(
            success_window,
            text="OK",
            command=lambda: [success_window.destroy(), self.show_dashboard()]
        )
        ok_btn.pack(pady=20)
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        current_mode = ctk.get_appearance_mode()
        new_mode = "dark" if current_mode == "Light" else "light"
        ctk.set_appearance_mode(new_mode)
