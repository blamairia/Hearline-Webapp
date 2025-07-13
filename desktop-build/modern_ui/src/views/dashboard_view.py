"""
Dashboard View for HeartLine Desktop Application
Replicates the dashboard from the Flask app with modern desktop components
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkinter
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np

class DashboardView(ctk.CTkScrollableFrame):
    """
    Modern dashboard view with statistics cards, charts, and recent data
    """
    
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.app = app
        self.setup_dashboard()
    
    def setup_dashboard(self):
        """Create the complete dashboard layout"""
        # Configure grid weights
        self.grid_columnconfigure((0, 1), weight=1)
        
        # Dashboard header with welcome message
        self.create_dashboard_header()
        
        # Statistics cards row
        self.create_stats_cards()
        
        # Charts and recent data row
        self.create_main_content()
        
        # Quick actions section
        self.create_quick_actions()
    
    def create_dashboard_header(self):
        """Create the dashboard header with welcome message"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 20))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Welcome message
        welcome_label = ctk.CTkLabel(
            header_frame,
            text=f"Welcome back, Dr. Admin! 👋",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.app.colors['text_dark']
        )
        welcome_label.grid(row=0, column=0, sticky="w")
        
        # Date and time
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        date_label = ctk.CTkLabel(
            header_frame,
            text=current_date,
            font=ctk.CTkFont(size=14),
            text_color=self.app.colors['text_light']
        )
        date_label.grid(row=1, column=0, sticky="w", pady=(5, 0))
        
        # Notification bell (placeholder)
        notification_btn = ctk.CTkButton(
            header_frame,
            text="🔔",
            font=ctk.CTkFont(size=20),
            width=40,
            height=40,
            corner_radius=20,
            fg_color=self.app.colors['white'],
            text_color=self.app.colors['primary'],
            hover_color=self.app.colors['background'],
            command=self.show_notifications
        )
        notification_btn.grid(row=0, column=2, sticky="e")
    
    def create_stats_cards(self):
        """Create statistics cards similar to the Flask dashboard"""
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 20))
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Sample statistics (would be fetched from database in real app)
        stats_data = [
            {"title": "Total Patients", "value": "1,247", "icon": "👥", "color": self.app.colors['primary'], "change": "+12%"},
            {"title": "Today's Visits", "value": "23", "icon": "📋", "color": self.app.colors['success'], "change": "+5%"},
            {"title": "Appointments", "value": "18", "icon": "📅", "color": self.app.colors['warning'], "change": "+8%"},
            {"title": "ECG Analyses", "value": "156", "icon": "💓", "color": self.app.colors['danger'], "change": "+15%"}
        ]
        
        for i, stat in enumerate(stats_data):
            card = self.create_stat_card(stats_frame, stat)
            card.grid(row=0, column=i, sticky="ew", padx=5)
    
    def create_stat_card(self, parent, stat_data):
        """Create an individual statistics card"""
        card = ctk.CTkFrame(
            parent,
            height=120,
            corner_radius=15,
            fg_color=self.app.colors['white']
        )
        card.grid_propagate(False)
        
        # Card content
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Icon and title row
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x")
        
        # Icon
        icon_label = ctk.CTkLabel(
            header_frame,
            text=stat_data['icon'],
            font=ctk.CTkFont(size=24),
            text_color=stat_data['color']
        )
        icon_label.pack(side="left")
        
        # Change indicator
        change_label = ctk.CTkLabel(
            header_frame,
            text=stat_data['change'],
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.app.colors['success'] if stat_data['change'].startswith('+') else self.app.colors['danger']
        )
        change_label.pack(side="right")
        
        # Value
        value_label = ctk.CTkLabel(
            content_frame,
            text=stat_data['value'],
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.app.colors['text_dark']
        )
        value_label.pack(pady=(10, 0))
        
        # Title
        title_label = ctk.CTkLabel(
            content_frame,
            text=stat_data['title'],
            font=ctk.CTkFont(size=12),
            text_color=self.app.colors['text_light']
        )
        title_label.pack()
        
        return card
    
    def create_main_content(self):
        """Create the main content area with charts and recent data"""
        main_content_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_content_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 20))
        main_content_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Recent patients card
        self.create_recent_patients_card(main_content_frame)
        
        # ECG analysis chart
        self.create_ecg_chart_card(main_content_frame)
    
    def create_recent_patients_card(self, parent):
        """Create the recent patients card"""
        card = ctk.CTkFrame(
            parent,
            corner_radius=15,
            fg_color=self.app.colors['white']
        )
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Card header
        header_frame = ctk.CTkFrame(card, fg_color="transparent", height=50)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="👥 Recent Patients",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.app.colors['text_dark']
        )
        title_label.pack(side="left", pady=10)
        
        view_all_btn = ctk.CTkButton(
            header_frame,
            text="View All",
            font=ctk.CTkFont(size=12),
            height=30,
            width=80,
            fg_color=self.app.colors['primary'],
            command=self.app.show_patients
        )
        view_all_btn.pack(side="right", pady=10)
        
        # Patient list
        list_frame = ctk.CTkScrollableFrame(card, height=300)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Sample recent patients (would be fetched from database)
        recent_patients = [
            {"name": "John Smith", "dob": "1985-03-15", "last_visit": "Today"},
            {"name": "Sarah Johnson", "dob": "1992-07-22", "last_visit": "Yesterday"},
            {"name": "Michael Brown", "dob": "1978-11-08", "last_visit": "2 days ago"},
            {"name": "Emily Davis", "dob": "1995-04-30", "last_visit": "3 days ago"},
            {"name": "Robert Wilson", "dob": "1968-12-03", "last_visit": "1 week ago"}
        ]
        
        for patient in recent_patients:
            self.create_patient_item(list_frame, patient)
    
    def create_patient_item(self, parent, patient_data):
        """Create a patient list item"""
        item_frame = ctk.CTkFrame(parent, fg_color=self.app.colors['background'], height=60)
        item_frame.pack(fill="x", pady=2)
        item_frame.pack_propagate(False)
        
        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Patient info
        name_label = ctk.CTkLabel(
            content_frame,
            text=patient_data['name'],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.app.colors['text_dark']
        )
        name_label.pack(anchor="w")
        
        details_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        details_frame.pack(fill="x", pady=(5, 0))
        
        dob_label = ctk.CTkLabel(
            details_frame,
            text=f"DOB: {patient_data['dob']}",
            font=ctk.CTkFont(size=11),
            text_color=self.app.colors['text_light']
        )
        dob_label.pack(side="left")
        
        visit_label = ctk.CTkLabel(
            details_frame,
            text=patient_data['last_visit'],
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.app.colors['primary']
        )
        visit_label.pack(side="right")
    
    def create_ecg_chart_card(self, parent):
        """Create the ECG analysis chart card"""
        card = ctk.CTkFrame(
            parent,
            corner_radius=15,
            fg_color=self.app.colors['white']
        )
        card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Card header
        header_frame = ctk.CTkFrame(card, fg_color="transparent", height=50)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="💓 ECG Analysis Trends",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.app.colors['text_dark']
        )
        title_label.pack(side="left", pady=10)
        
        # Chart frame
        chart_frame = ctk.CTkFrame(card, fg_color="transparent")
        chart_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Create matplotlib chart
        self.create_ecg_trend_chart(chart_frame)
    
    def create_ecg_trend_chart(self, parent):
        """Create a trend chart for ECG analyses"""
        # Create figure
        fig, ax = plt.subplots(figsize=(6, 3), facecolor='white')
        
        # Sample data (would be fetched from database)
        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        analyses = np.random.poisson(5, 30) + np.random.randint(0, 3, 30)
        
        # Plot
        ax.plot(dates, analyses, color=self.app.colors['primary'], linewidth=2, marker='o', markersize=4)
        ax.fill_between(dates, analyses, alpha=0.3, color=self.app.colors['primary'])
        
        # Styling
        ax.set_title('Daily ECG Analyses (Last 30 Days)', fontsize=12, fontweight='bold', pad=20)
        ax.set_xlabel('Date', fontsize=10)
        ax.set_ylabel('Number of Analyses', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Format dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkinter(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def create_quick_actions(self):
        """Create quick action buttons"""
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 20))
        
        # Title
        title_label = ctk.CTkLabel(
            actions_frame,
            text="⚡ Quick Actions",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.app.colors['text_dark']
        )
        title_label.pack(anchor="w", pady=(0, 15))
        
        # Actions grid
        actions_grid = ctk.CTkFrame(actions_frame, fg_color="transparent")
        actions_grid.pack(fill="x")
        actions_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Quick action buttons
        quick_actions = [
            {"text": "New Patient", "icon": "👤", "color": self.app.colors['primary'], "command": self.app.show_new_patient},
            {"text": "Schedule Appointment", "icon": "📅", "color": self.app.colors['success'], "command": self.app.show_appointments},
            {"text": "Upload ECG", "icon": "💓", "color": self.app.colors['danger'], "command": self.app.show_new_visit},
            {"text": "Generate Report", "icon": "📊", "color": self.app.colors['warning'], "command": self.show_reports}
        ]
        
        for i, action in enumerate(quick_actions):
            btn = ctk.CTkButton(
                actions_grid,
                text=f"{action['icon']}\\n{action['text']}",
                font=ctk.CTkFont(size=14, weight="bold"),
                height=80,
                corner_radius=15,
                fg_color=action['color'],
                command=action['command']
            )
            btn.grid(row=0, column=i, sticky="ew", padx=5)
    
    def show_notifications(self):
        """Show notifications (placeholder)"""
        # Could open a popup or side panel with notifications
        print("Notifications clicked")
    
    def show_reports(self):
        """Show reports section (placeholder)"""
        print("Reports clicked")
