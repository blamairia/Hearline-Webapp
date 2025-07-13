"""
Visits Table View for HeartLine Desktop Application
Modern visits table with search, filtering, and medical data
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import threading

class VisitsTableView(ctk.CTkFrame):
    """
    Modern visits table with medical data, search, and filtering capabilities
    """
    
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.app = app
        self.visits_data = []
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
            text="🏥 Patient Visits",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.app.colors['text_dark']
        )
        title_label.pack(side="left")
        
        # Visit count badge
        count_badge = ctk.CTkFrame(
            title_frame,
            corner_radius=15,
            fg_color=self.app.colors['success']
        )
        count_badge.pack(side="left", padx=(15, 0))
        
        count_label = ctk.CTkLabel(
            count_badge,
            text="2,843 Total",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.app.colors['white']
        )
        count_label.pack(padx=12, pady=6)
        
        # Action buttons
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=2, sticky="e")
        
        # Export button
        export_btn = ctk.CTkButton(
            actions_frame,
            text="� Export",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=100,
            height=35,
            corner_radius=8,
            fg_color=self.app.colors['success'],
            hover_color="#218838",
            command=self.export_data
        )
        export_btn.pack(side="right", padx=(5, 0))
        
        # New visit button
        add_btn = ctk.CTkButton(
            actions_frame,
            text="➕ New Visit",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=120,
            height=35,
            corner_radius=8,
            fg_color=self.app.colors['primary'],
            hover_color=self.app.colors['primary_dark'],
            command=self.app.show_new_visit
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
            placeholder_text="🔍 Search visits by patient name, diagnosis, or doctor...",
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            textvariable=self.search_var
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_var.trace("w", self.on_search_change)
        
        # Date range filter
        date_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        date_frame.grid(row=0, column=1, padx=(0, 10))
        
        date_label = ctk.CTkLabel(
            date_frame,
            text="Date Range:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.app.colors['text_dark']
        )
        date_label.pack()
        
        self.date_filter = ctk.CTkComboBox(
            date_frame,
            values=["All Time", "Today", "This Week", "This Month", "Last 3 Months", "This Year"],
            width=120,
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=11),
            command=self.apply_filters
        )
        self.date_filter.set("All Time")
        self.date_filter.pack()
        
        # Visit type filter
        type_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        type_frame.grid(row=0, column=2, padx=(0, 10))
        
        type_label = ctk.CTkLabel(
            type_frame,
            text="Visit Type:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.app.colors['text_dark']
        )
        type_label.pack()
        
        self.type_filter = ctk.CTkComboBox(
            type_frame,
            values=["All", "Consultation", "Follow-up", "Emergency", "Checkup", "Surgery"],
            width=110,
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=11),
            command=self.apply_filters
        )
        self.type_filter.set("All")
        self.type_filter.pack()
        
        # Clear filters button
        clear_btn = ctk.CTkButton(
            search_frame,
            text="🗑️",
            width=40,
            height=40,
            corner_radius=8,
            fg_color=self.app.colors['text_light'],
            hover_color="#5a6268",
            command=self.clear_filters
        )
        clear_btn.grid(row=0, column=3)
    
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
        style.configure("Visits.Treeview",
                       background=self.app.colors['white'],
                       foreground=self.app.colors['text_dark'],
                       fieldbackground=self.app.colors['white'],
                       borderwidth=0,
                       font=('Segoe UI', 10))
        
        style.configure("Visits.Treeview.Heading",
                       background=self.app.colors['success'],
                       foreground=self.app.colors['white'],
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0)
        
        style.map("Visits.Treeview",
                 background=[("selected", self.app.colors['background'])],
                 foreground=[("selected", self.app.colors['text_dark'])])
        
        # Create treeview
        columns = ("ID", "Date", "Patient", "Doctor", "Type", "Diagnosis", "Status", "Follow-up", "Actions")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            style="Visits.Treeview",
            height=15
        )
        
        # Configure columns
        column_widths = {
            "ID": 80, "Date": 100, "Patient": 150, "Doctor": 120,
            "Type": 100, "Diagnosis": 200, "Status": 100, "Follow-up": 100, "Actions": 150
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
            text="Showing 1-25 of 2,843 visits",
            font=ctk.CTkFont(size=12),
            text_color=self.app.colors['text_light']
        )
        self.results_label.grid(row=0, column=0, sticky="w")
        
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
            text="Page 1 of 114",
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
        """Load sample visit data"""
        # Sample data (in real app, this would come from database)
        self.visits_data = [
            {
                "id": 1, "date": "2024-07-10", "patient": "John Smith", "doctor": "Dr. Wilson",
                "type": "Consultation", "diagnosis": "Hypertension", "status": "Completed", "follow_up": "2024-08-10"
            },
            {
                "id": 2, "date": "2024-07-10", "patient": "Sarah Johnson", "doctor": "Dr. Brown",
                "type": "Follow-up", "diagnosis": "Diabetes Type 2", "status": "Completed", "follow_up": "2024-08-15"
            },
            {
                "id": 3, "date": "2024-07-09", "patient": "Michael Brown", "doctor": "Dr. Davis",
                "type": "Emergency", "diagnosis": "Chest Pain", "status": "Admitted", "follow_up": "2024-07-12"
            },
            {
                "id": 4, "date": "2024-07-09", "patient": "Emily Davis", "doctor": "Dr. Wilson",
                "type": "Checkup", "diagnosis": "Annual Physical", "status": "Completed", "follow_up": "2025-07-09"
            },
            {
                "id": 5, "date": "2024-07-08", "patient": "Robert Wilson", "doctor": "Dr. Martinez",
                "type": "Surgery", "diagnosis": "Gallbladder Removal", "status": "Scheduled", "follow_up": "2024-07-20"
            },
            {
                "id": 6, "date": "2024-07-08", "patient": "Lisa Anderson", "doctor": "Dr. Brown",
                "type": "Consultation", "diagnosis": "Migraine", "status": "Completed", "follow_up": "2024-08-08"
            }
        ]
        
        self.filtered_data = self.visits_data.copy()
        self.populate_table()
    
    def populate_table(self):
        """Populate the table with data"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add new data
        for visit in self.filtered_data:
            values = (
                visit["id"],
                visit["date"],
                visit["patient"],
                visit["doctor"],
                visit["type"],
                visit["diagnosis"],
                visit["status"],
                visit["follow_up"],
                "View • Edit • Delete"
            )
            
            # Add row with status-based styling
            item = self.tree.insert("", "end", values=values)
            
            # Color coding based on status
            if visit["status"] == "Emergency" or visit["status"] == "Admitted":
                # Emergency status styling would go here
                pass
    
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
        type_filter = self.type_filter.get()
        
        # Filter data
        self.filtered_data = []
        for visit in self.visits_data:
            # Search filter
            if search_term:
                searchable_text = f"{visit['patient']} {visit['doctor']} {visit['diagnosis']} {visit['type']}".lower()
                if search_term not in searchable_text:
                    continue
            
            # Type filter
            if type_filter != "All" and visit['type'] != type_filter:
                continue
            
            # Date filter (simplified - in real app would use actual date parsing)
            if date_filter != "All Time":
                # This would include actual date filtering logic
                pass
            
            self.filtered_data.append(visit)
        
        # Update table
        self.populate_table()
        
        # Update results label
        total = len(self.filtered_data)
        self.results_label.configure(text=f"Showing {min(25, total)} of {total} visits")
    
    def clear_filters(self):
        """Clear all filters and search"""
        self.search_var.set("")
        self.date_filter.set("All Time")
        self.type_filter.set("All")
        self.apply_filters()
    
    def on_row_double_click(self, event):
        """Handle double-click on table row"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            visit_id = item['values'][0]
            self.view_visit_details(visit_id)
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        # Select the row under cursor
        row_id = self.tree.identify_row(event.y)
        if row_id:
            self.tree.selection_set(row_id)
            
            # Create context menu
            context_menu = tk.Menu(self, tearoff=0)
            context_menu.add_command(label="👁️ View Details", command=lambda: self.view_visit_details())
            context_menu.add_command(label="✏️ Edit Visit", command=lambda: self.edit_visit())
            context_menu.add_separator()
            context_menu.add_command(label="📋 Duplicate Visit", command=lambda: self.duplicate_visit())
            context_menu.add_command(label="📄 Generate Report", command=lambda: self.generate_report())
            context_menu.add_separator()
            context_menu.add_command(label="🗑️ Delete Visit", command=lambda: self.delete_visit())
            
            # Show menu
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
    
    def view_visit_details(self, visit_id=None):
        """View visit details"""
        if not visit_id:
            selection = self.tree.selection()
            if selection:
                visit_id = self.tree.item(selection[0])['values'][0]
        
        if visit_id:
            messagebox.showinfo("Visit Details", f"Opening details for visit ID: {visit_id}")
    
    def edit_visit(self):
        """Edit selected visit"""
        selection = self.tree.selection()
        if selection:
            visit_id = self.tree.item(selection[0])['values'][0]
            messagebox.showinfo("Edit Visit", f"Opening edit form for visit ID: {visit_id}")
    
    def duplicate_visit(self):
        """Duplicate selected visit"""
        selection = self.tree.selection()
        if selection:
            visit_id = self.tree.item(selection[0])['values'][0]
            messagebox.showinfo("Duplicate Visit", f"Creating duplicate of visit ID: {visit_id}")
    
    def generate_report(self):
        """Generate report for selected visit"""
        selection = self.tree.selection()
        if selection:
            visit_id = self.tree.item(selection[0])['values'][0]
            messagebox.showinfo("Generate Report", f"Generating report for visit ID: {visit_id}")
    
    def delete_visit(self):
        """Delete selected visit"""
        selection = self.tree.selection()
        if selection:
            patient_name = self.tree.item(selection[0])['values'][2]
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this visit for '{patient_name}'?\n\nThis action cannot be undone."):
                # In real app, delete from database
                self.tree.delete(selection[0])
                messagebox.showinfo("Success", "Visit has been deleted.")
    
    def export_data(self):
        """Export table data"""
        messagebox.showinfo("Export", "Exporting visit data to CSV file...")
    
    def previous_page(self):
        """Go to previous page"""
        print("Previous page clicked")
    
    def next_page(self):
        """Go to next page"""
        print("Next page clicked")
