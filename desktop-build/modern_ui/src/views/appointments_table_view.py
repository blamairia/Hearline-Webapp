"""
Appointments Table View for HeartLine Desktop Application
Modern appointments table with calendar integration and scheduling
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta
import threading

class AppointmentsTableView(ctk.CTkFrame):
    """
    Modern appointments table with calendar view, scheduling, and management capabilities
    """
    
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.app = app
        self.appointments_data = []
        self.filtered_data = []
        self.setup_table_view()
        self.load_sample_data()
    
    def setup_table_view(self):
        """Create the complete table view layout"""
        # Configure grid weights
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Table header with search and filters
        self.create_table_header()
        
        # Table controls (search, filter, actions)
        self.create_table_controls()
        
        # Main data table
        self.create_data_table()
        
        # Table pagination
        self.create_pagination()
    
    def create_table_header(self):
        """Create the table header with title and quick actions"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title and stats
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="📅 Appointments Schedule",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.app.colors['text_dark']
        )
        title_label.pack(side="left")
        
        # Today's appointments badge
        count_badge = ctk.CTkFrame(
            title_frame,
            corner_radius=15,
            fg_color=self.app.colors['warning']
        )
        count_badge.pack(side="left", padx=(15, 0))
        
        count_label = ctk.CTkLabel(
            count_badge,
            text="8 Today",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.app.colors['white']
        )
        count_label.pack(padx=12, pady=6)
        
        # Upcoming badge
        upcoming_badge = ctk.CTkFrame(
            title_frame,
            corner_radius=15,
            fg_color=self.app.colors['info']
        )
        upcoming_badge.pack(side="left", padx=(10, 0))
        
        upcoming_label = ctk.CTkLabel(
            upcoming_badge,
            text="24 This Week",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.app.colors['white']
        )
        upcoming_label.pack(padx=12, pady=6)
        
        # Action buttons
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=2, sticky="e")
        
        # Calendar view button
        calendar_btn = ctk.CTkButton(
            actions_frame,
            text="📆 Calendar",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=100,
            height=35,
            corner_radius=8,
            fg_color=self.app.colors['info'],
            hover_color="#0056b3",
            command=self.show_calendar_view
        )
        calendar_btn.pack(side="right", padx=(5, 0))
        
        # New appointment button
        add_btn = ctk.CTkButton(
            actions_frame,
            text="➕ Schedule",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=120,
            height=35,
            corner_radius=8,
            fg_color=self.app.colors['primary'],
            hover_color=self.app.colors['primary_dark'],
            command=self.schedule_new_appointment
        )
        add_btn.pack(side="right", padx=(5, 0))
    
    def create_table_controls(self):
        """Create search and filter controls"""
        controls_frame = ctk.CTkFrame(
            self,
            corner_radius=10,
            fg_color=self.app.colors['white']
        )
        controls_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        controls_frame.grid_columnconfigure(0, weight=1)
        
        # Controls content
        controls_content = ctk.CTkFrame(controls_frame, fg_color="transparent")
        controls_content.pack(fill="x", padx=20, pady=15)
        controls_content.grid_columnconfigure(0, weight=1)
        
        # Search and filters row
        search_frame = ctk.CTkFrame(controls_content, fg_color="transparent")
        search_frame.grid(row=0, column=0, sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search appointments by patient, doctor, or time...",
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            textvariable=self.search_var
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_var.trace("w", self.on_search_change)
        
        # Date filter
        date_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        date_frame.grid(row=0, column=1, padx=(0, 10))
        
        date_label = ctk.CTkLabel(
            date_frame,
            text="Date:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.app.colors['text_dark']
        )
        date_label.pack()
        
        self.date_filter = ctk.CTkComboBox(
            date_frame,
            values=["All", "Today", "Tomorrow", "This Week", "Next Week", "This Month"],
            width=110,
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=11),
            command=self.apply_filters
        )
        self.date_filter.set("All")
        self.date_filter.pack()
        
        # Status filter
        status_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        status_frame.grid(row=0, column=2, padx=(0, 10))
        
        status_label = ctk.CTkLabel(
            status_frame,
            text="Status:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.app.colors['text_dark']
        )
        status_label.pack()
        
        self.status_filter = ctk.CTkComboBox(
            status_frame,
            values=["All", "Scheduled", "Confirmed", "In Progress", "Completed", "Cancelled", "No Show"],
            width=100,
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=11),
            command=self.apply_filters
        )
        self.status_filter.set("All")
        self.status_filter.pack()
        
        # Doctor filter
        doctor_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        doctor_frame.grid(row=0, column=3, padx=(0, 10))
        
        doctor_label = ctk.CTkLabel(
            doctor_frame,
            text="Doctor:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.app.colors['text_dark']
        )
        doctor_label.pack()
        
        self.doctor_filter = ctk.CTkComboBox(
            doctor_frame,
            values=["All", "Dr. Wilson", "Dr. Brown", "Dr. Davis", "Dr. Martinez", "Dr. Johnson"],
            width=100,
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=11),
            command=self.apply_filters
        )
        self.doctor_filter.set("All")
        self.doctor_filter.pack()
        
        # Clear filters button
        clear_btn = ctk.CTkButton(
            search_frame,
            text="�️",
            width=40,
            height=40,
            corner_radius=8,
            fg_color=self.app.colors['text_light'],
            hover_color="#5a6268",
            command=self.clear_filters
        )
        clear_btn.grid(row=0, column=4)
    
    def create_data_table(self):
        """Create the main data table with modern styling"""
        # Table container
        table_container = ctk.CTkFrame(
            self,
            corner_radius=10,
            fg_color=self.app.colors['white']
        )
        table_container.grid(row=2, column=0, sticky="nsew", padx=20)
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
        
        # Create treeview with scrollbars
        tree_frame = ctk.CTkFrame(table_container, fg_color="transparent")
        tree_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Configure treeview style
        style = ttk.Style()
        style.theme_use("clam")
        
        # Customize treeview colors
        style.configure("Appointments.Treeview",
                       background=self.app.colors['white'],
                       foreground=self.app.colors['text_dark'],
                       fieldbackground=self.app.colors['white'],
                       borderwidth=0,
                       font=('Segoe UI', 10))
        
        style.configure("Appointments.Treeview.Heading",
                       background=self.app.colors['warning'],
                       foreground=self.app.colors['white'],
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0)
        
        style.map("Appointments.Treeview",
                 background=[("selected", self.app.colors['background'])],
                 foreground=[("selected", self.app.colors['text_dark'])])
        
        # Create treeview
        columns = ("ID", "Date", "Time", "Patient", "Doctor", "Type", "Duration", "Status", "Notes", "Actions")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            style="Appointments.Treeview",
            height=15
        )
        
        # Configure columns
        column_widths = {
            "ID": 60, "Date": 100, "Time": 80, "Patient": 150, "Doctor": 120,
            "Type": 100, "Duration": 80, "Status": 100, "Notes": 150, "Actions": 120
        }
        
        for col in columns:
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, width=column_widths.get(col, 100), anchor="w")
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Bind events
        self.tree.bind("<Double-Button-1>", self.on_row_double_click)
        self.tree.bind("<Button-3>", self.show_context_menu)  # Right click
    
    def create_pagination(self):
        """Create pagination controls"""
        pagination_frame = ctk.CTkFrame(self, fg_color="transparent")
        pagination_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(10, 20))
        pagination_frame.grid_columnconfigure(1, weight=1)
        
        # Results info
        self.results_label = ctk.CTkLabel(
            pagination_frame,
            text="Showing 1-25 of 156 appointments",
            font=ctk.CTkFont(size=12),
            text_color=self.app.colors['text_light']
        )
        self.results_label.grid(row=0, column=0, sticky="w")
        
        # Quick actions
        quick_actions = ctk.CTkFrame(pagination_frame, fg_color="transparent")
        quick_actions.grid(row=0, column=1)
        
        # Mark completed button
        complete_btn = ctk.CTkButton(
            quick_actions,
            text="✅ Mark Completed",
            width=120,
            height=30,
            font=ctk.CTkFont(size=11),
            fg_color=self.app.colors['success'],
            hover_color="#218838",
            command=self.mark_completed
        )
        complete_btn.pack(side="left", padx=5)
        
        # Send reminders button
        reminder_btn = ctk.CTkButton(
            quick_actions,
            text="📧 Send Reminders",
            width=120,
            height=30,
            font=ctk.CTkFont(size=11),
            fg_color=self.app.colors['info'],
            hover_color="#0056b3",
            command=self.send_reminders
        )
        reminder_btn.pack(side="left", padx=5)
        
        # Page controls
        page_frame = ctk.CTkFrame(pagination_frame, fg_color="transparent")
        page_frame.grid(row=0, column=2, sticky="e")
        
        # Previous button
        prev_btn = ctk.CTkButton(
            page_frame,
            text="◀ Previous",
            width=80,
            height=30,
            font=ctk.CTkFont(size=11),
            fg_color=self.app.colors['background'],
            text_color=self.app.colors['text_dark'],
            hover_color=self.app.colors['text_light'],
            command=self.previous_page
        )
        prev_btn.pack(side="left", padx=(0, 5))
        
        # Page info
        self.page_label = ctk.CTkLabel(
            page_frame,
            text="Page 1 of 7",
            font=ctk.CTkFont(size=12),
            text_color=self.app.colors['text_dark']
        )
        self.page_label.pack(side="left", padx=10)
        
        # Next button
        next_btn = ctk.CTkButton(
            page_frame,
            text="Next ▶",
            width=80,
            height=30,
            font=ctk.CTkFont(size=11),
            fg_color=self.app.colors['background'],
            text_color=self.app.colors['text_dark'],
            hover_color=self.app.colors['text_light'],
            command=self.next_page
        )
        next_btn.pack(side="left", padx=(5, 0))
    
    def load_sample_data(self):
        """Load sample appointment data"""
        # Sample data (in real app, this would come from database)
        today = datetime.now()
        self.appointments_data = [
            {
                "id": 1, "date": today.strftime("%Y-%m-%d"), "time": "09:00", 
                "patient": "John Smith", "doctor": "Dr. Wilson", "type": "Consultation",
                "duration": "30 min", "status": "Scheduled", "notes": "Follow-up for hypertension"
            },
            {
                "id": 2, "date": today.strftime("%Y-%m-%d"), "time": "10:30", 
                "patient": "Sarah Johnson", "doctor": "Dr. Brown", "type": "Checkup",
                "duration": "45 min", "status": "Confirmed", "notes": "Annual physical exam"
            },
            {
                "id": 3, "date": (today + timedelta(days=1)).strftime("%Y-%m-%d"), "time": "14:00", 
                "patient": "Michael Brown", "doctor": "Dr. Davis", "type": "Surgery",
                "duration": "120 min", "status": "Scheduled", "notes": "Pre-op consultation"
            },
            {
                "id": 4, "date": today.strftime("%Y-%m-%d"), "time": "11:15", 
                "patient": "Emily Davis", "doctor": "Dr. Martinez", "type": "Follow-up",
                "duration": "20 min", "status": "In Progress", "notes": "Diabetes management"
            },
            {
                "id": 5, "date": (today + timedelta(days=2)).strftime("%Y-%m-%d"), "time": "16:30", 
                "patient": "Robert Wilson", "doctor": "Dr. Johnson", "type": "Emergency",
                "duration": "60 min", "status": "Cancelled", "notes": "Patient rescheduled"
            },
            {
                "id": 6, "date": today.strftime("%Y-%m-%d"), "time": "08:30", 
                "patient": "Lisa Anderson", "doctor": "Dr. Wilson", "type": "Consultation",
                "duration": "30 min", "status": "Completed", "notes": "New patient intake"
            }
        ]
        
        self.filtered_data = self.appointments_data.copy()
        self.populate_table()
    
    def populate_table(self):
        """Populate the table with data"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add new data
        for appointment in self.filtered_data:
            values = (
                appointment["id"],
                appointment["date"],
                appointment["time"],
                appointment["patient"],
                appointment["doctor"],
                appointment["type"],
                appointment["duration"],
                appointment["status"],
                appointment["notes"],
                "View • Edit • Cancel"
            )
            
            # Add row with status-based styling
            item = self.tree.insert("", "end", values=values)
    
    def on_search_change(self, *args):
        """Handle search input changes"""
        # Debounce search to avoid too many calls
        if hasattr(self, '_search_timer'):
            self.after_cancel(self._search_timer)
        self._search_timer = self.after(300, self.apply_filters)
    
    def apply_filters(self, *args):
        """Apply search and filter criteria"""
        search_term = self.search_var.get().lower()
        date_filter = self.date_filter.get()
        status_filter = self.status_filter.get()
        doctor_filter = self.doctor_filter.get()
        
        # Filter data
        self.filtered_data = []
        for appointment in self.appointments_data:
            # Search filter
            if search_term:
                searchable_text = f"{appointment['patient']} {appointment['doctor']} {appointment['type']} {appointment['time']}".lower()
                if search_term not in searchable_text:
                    continue
            
            # Status filter
            if status_filter != "All" and appointment['status'] != status_filter:
                continue
            
            # Doctor filter
            if doctor_filter != "All" and appointment['doctor'] != doctor_filter:
                continue
            
            # Date filter (simplified - in real app would use actual date parsing)
            if date_filter != "All":
                today = datetime.now().strftime("%Y-%m-%d")
                if date_filter == "Today" and appointment['date'] != today:
                    continue
                # Add more date filtering logic as needed
            
            self.filtered_data.append(appointment)
        
        # Update table
        self.populate_table()
        
        # Update results label
        total = len(self.filtered_data)
        self.results_label.configure(text=f"Showing {min(25, total)} of {total} appointments")
    
    def clear_filters(self):
        """Clear all filters and search"""
        self.search_var.set("")
        self.date_filter.set("All")
        self.status_filter.set("All")
        self.doctor_filter.set("All")
        self.apply_filters()
    
    def on_row_double_click(self, event):
        """Handle double-click on table row"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            appointment_id = item['values'][0]
            self.view_appointment_details(appointment_id)
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        # Select the row under cursor
        row_id = self.tree.identify_row(event.y)
        if row_id:
            self.tree.selection_set(row_id)
            
            # Create context menu
            context_menu = tk.Menu(self, tearoff=0)
            context_menu.add_command(label="👁️ View Details", command=lambda: self.view_appointment_details())
            context_menu.add_command(label="✏️ Edit Appointment", command=lambda: self.edit_appointment())
            context_menu.add_separator()
            context_menu.add_command(label="✅ Mark Completed", command=lambda: self.mark_appointment_completed())
            context_menu.add_command(label="📧 Send Reminder", command=lambda: self.send_reminder())
            context_menu.add_command(label="🔄 Reschedule", command=lambda: self.reschedule_appointment())
            context_menu.add_separator()
            context_menu.add_command(label="❌ Cancel Appointment", command=lambda: self.cancel_appointment())
            
            # Show menu
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
    
    def view_appointment_details(self, appointment_id=None):
        """View appointment details"""
        if not appointment_id:
            selection = self.tree.selection()
            if selection:
                appointment_id = self.tree.item(selection[0])['values'][0]
        
        if appointment_id:
            messagebox.showinfo("Appointment Details", f"Opening details for appointment ID: {appointment_id}")
    
    def edit_appointment(self):
        """Edit selected appointment"""
        selection = self.tree.selection()
        if selection:
            appointment_id = self.tree.item(selection[0])['values'][0]
            messagebox.showinfo("Edit Appointment", f"Opening edit form for appointment ID: {appointment_id}")
    
    def mark_appointment_completed(self):
        """Mark selected appointment as completed"""
        selection = self.tree.selection()
        if selection:
            appointment_id = self.tree.item(selection[0])['values'][0]
            messagebox.showinfo("Mark Completed", f"Marking appointment ID {appointment_id} as completed")
    
    def send_reminder(self):
        """Send reminder for selected appointment"""
        selection = self.tree.selection()
        if selection:
            patient_name = self.tree.item(selection[0])['values'][3]
            messagebox.showinfo("Send Reminder", f"Sending reminder to {patient_name}")
    
    def reschedule_appointment(self):
        """Reschedule selected appointment"""
        selection = self.tree.selection()
        if selection:
            appointment_id = self.tree.item(selection[0])['values'][0]
            messagebox.showinfo("Reschedule", f"Opening reschedule dialog for appointment ID: {appointment_id}")
    
    def cancel_appointment(self):
        """Cancel selected appointment"""
        selection = self.tree.selection()
        if selection:
            patient_name = self.tree.item(selection[0])['values'][3]
            if messagebox.askyesno("Confirm Cancel", f"Are you sure you want to cancel the appointment for '{patient_name}'?"):
                # In real app, update database
                messagebox.showinfo("Success", "Appointment has been cancelled.")
    
    def schedule_new_appointment(self):
        """Schedule a new appointment"""
        messagebox.showinfo("Schedule Appointment", "Opening appointment scheduling form...")
    
    def show_calendar_view(self):
        """Show calendar view"""
        messagebox.showinfo("Calendar View", "Opening calendar view...")
    
    def mark_completed(self):
        """Mark selected appointments as completed"""
        messagebox.showinfo("Mark Completed", "Marking selected appointments as completed...")
    
    def send_reminders(self):
        """Send reminders to patients"""
        messagebox.showinfo("Send Reminders", "Sending appointment reminders...")
    
    def previous_page(self):
        """Go to previous page"""
        print("Previous page clicked")
    
    def next_page(self):
        """Go to next page"""
        print("Next page clicked")
