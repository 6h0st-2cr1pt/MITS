import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database import add_missing_item, get_missing_items

class MissingItemsFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Role-based access control
        if self.controller.user_role != "staff":
            self.create_access_denied()
            return
        
        # Title and search area
        self.create_header()
        
        # Main content split into two panes
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left side - Items list
        self.create_items_list(paned)
        
        # Right side - Item details/form
        self.create_item_form(paned)
        
        # Load initial data
        self.load_items()
    
    def create_access_denied(self):
        """Create access denied message for unauthorized users"""
        access_frame = ttk.Frame(self, padding=50)
        access_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        ttk.Label(
            access_frame,
            text="Access Denied",
            font=('Helvetica', 24, 'bold')
        ).pack(pady=(0, 20))
        
        ttk.Label(
            access_frame,
            text="You don't have permission to access this feature.",
            font=('Helvetica', 12)
        ).pack()
        
        ttk.Label(
            access_frame,
            text="Please contact an administrator if you need access.",
            font=('Helvetica', 12)
        ).pack(pady=(10, 0))
    
    def create_header(self):
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        ttk.Label(
            header_frame, 
            text="Missing Items",
            font=('Helvetica', 20, 'bold')
        ).pack(side=tk.LEFT)
        
        # Search area
        search_frame = ttk.Frame(header_frame)
        search_frame.pack(side=tk.RIGHT)
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=25)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            search_frame,
            text="Search",
            style='info.TButton',
            command=self.search_items
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            search_frame,
            text="Clear",
            style='secondary.TButton',
            command=self.clear_search
        ).pack(side=tk.LEFT, padx=5)
    
    def create_items_list(self, parent):
        list_frame = ttk.Frame(parent)
        parent.add(list_frame, weight=1)
        
        # Items list with scrollbar
        columns = ("id", "item_name", "student_id", "date_reported", "status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=20)
        
        # Configure columns
        self.tree.heading("id", text="ID")
        self.tree.heading("item_name", text="Item Name")
        self.tree.heading("student_id", text="Student ID")
        self.tree.heading("date_reported", text="Date Reported")
        self.tree.heading("status", text="Status")
        
        self.tree.column("id", width=50)
        self.tree.column("item_name", width=150)
        self.tree.column("student_id", width=100)
        self.tree.column("date_reported", width=150)
        self.tree.column("status", width=100)
        
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack items
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_item_form(self, parent):
        form_frame = ttk.Frame(parent, padding=10)
        parent.add(form_frame, weight=1)
        
        # Form title
        ttk.Label(
            form_frame, 
            text="Report Missing Item",
            font=('Helvetica', 16, 'bold')
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Form fields
        fields_frame = ttk.Frame(form_frame)
        fields_frame.pack(fill=tk.BOTH, expand=True)
        
        # Student ID
        ttk.Label(fields_frame, text="Student ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.student_id_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=self.student_id_var, width=30).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Item Name
        ttk.Label(fields_frame, text="Item Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.item_name_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=self.item_name_var, width=30).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Color
        ttk.Label(fields_frame, text="Color:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.color_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=self.color_var, width=30).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Location
        ttk.Label(fields_frame, text="Last Seen Location:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.location_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=self.location_var, width=30).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Description
        ttk.Label(fields_frame, text="Description:").grid(row=4, column=0, sticky=tk.NW, pady=5)
        self.description_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=self.description_var, width=30).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            button_frame,
            text="Submit Report",
            style='success.TButton',
            command=self.submit_report
        ).pack(side=tk.RIGHT)
        
        ttk.Button(
            button_frame,
            text="Clear Form",
            style='secondary.TButton',
            command=self.clear_form
        ).pack(side=tk.RIGHT, padx=5)
    
    def load_items(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get items from database
        items = get_missing_items(self.controller.db_path, self.search_var.get())
        
        # Add items to treeview
        for item in items:
            self.tree.insert("", tk.END, values=(
                item["id"],
                item["item_name"],
                item["student_id"],
                item["date_reported"],
                item["status"]
            ))
    
    def search_items(self):
        self.load_items()
    
    def clear_search(self):
        self.search_var.set("")
        self.load_items()
    
    def on_item_select(self, event):
        # Get selected item
        try:
            selected_id = self.tree.item(self.tree.selection()[0], "values")[0]
            # You could load the item details into the form here
        except IndexError:
            pass
    
    def submit_report(self):
        # Get form data
        student_id = self.student_id_var.get().strip()
        item_name = self.item_name_var.get().strip()
        color = self.color_var.get().strip()
        location = self.location_var.get().strip()
        description = self.description_var.get().strip()
        
        # Validate form
        if not student_id or not item_name:
            messagebox.showerror("Error", "Student ID and Item Name are required")
            return
        
        # Add item to database
        success = add_missing_item(
            self.controller.db_path,
            self.controller.current_user,
            student_id,
            item_name,
            description,
            color,
            location
        )
        
        if success:
            messagebox.showinfo("Success", "Missing item reported successfully")
            self.clear_form()
            self.load_items()
    
    def clear_form(self):
        self.student_id_var.set("")
        self.item_name_var.set("")
        self.color_var.set("")
        self.location_var.set("")
        self.description_var.set("")
