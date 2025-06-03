import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database import get_claim_requests, approve_claim

class ClaimRequestsFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Title and filters
        self.create_header()
        
        # Create main content area
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create requests list
        self.create_requests_list(main_frame)
        
        # Create action buttons
        self.create_action_buttons(main_frame)
        
        # Load initial data
        self.load_requests()
    
    def create_header(self):
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        ttk.Label(
            header_frame, 
            text="Claim Requests",
            font=('Helvetica', 20, 'bold')
        ).pack(side=tk.LEFT)
        
        # Filter area
        filter_frame = ttk.Frame(header_frame)
        filter_frame.pack(side=tk.RIGHT)
        
        ttk.Label(filter_frame, text="Status:").pack(side=tk.LEFT)
        
        self.status_var = tk.StringVar(value="All")
        status_menu = ttk.OptionMenu(
            filter_frame,
            self.status_var,
            "All",
            "All",
            "Pending",
            "Approved",
            "Rejected"
        )
        status_menu.pack(side=tk.LEFT, padx=5)
        
        # Apply filter button
        ttk.Button(
            filter_frame,
            text="Apply Filter",
            style='info.TButton',
            command=self.load_requests
        ).pack(side=tk.LEFT, padx=5)
    
    def create_requests_list(self, parent):
        # Requests list with scrollbar
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("id", "student_id", "student_name", "item_name", "requested_by", "date_requested", "status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=20)
        
        # Configure columns
        self.tree.heading("id", text="ID")
        self.tree.heading("student_id", text="Student ID")
        self.tree.heading("student_name", text="Student Name")
        self.tree.heading("item_name", text="Item Name")
        self.tree.heading("requested_by", text="Requested By")
        self.tree.heading("date_requested", text="Date Requested")
        self.tree.heading("status", text="Status")
        
        self.tree.column("id", width=50)
        self.tree.column("student_id", width=100)
        self.tree.column("student_name", width=150)
        self.tree.column("item_name", width=150)
        self.tree.column("requested_by", width=100)
        self.tree.column("date_requested", width=150)
        self.tree.column("status", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack items
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_action_buttons(self, parent):
        button_frame = ttk.Frame(parent, padding=10)
        button_frame.pack(fill=tk.X)
        
        # Only admins can approve/verify claims
        if self.controller.user_role == "admin":
            ttk.Button(
                button_frame,
                text="Approve Claim",
                style='success.TButton',
                command=self.approve_request
            ).pack(side=tk.RIGHT, padx=5)
            
            ttk.Button(
                button_frame,
                text="Reject Claim",
                style='danger.TButton',
                command=self.reject_request
            ).pack(side=tk.RIGHT, padx=5)
        
        # Staff can only submit claims
        elif self.controller.user_role == "staff":
            ttk.Button(
                button_frame,
                text="Submit New Claim",
                style='primary.TButton',
                command=self.submit_new_claim
            ).pack(side=tk.RIGHT, padx=5)
    
    def submit_new_claim(self):
        # This would open a dialog to submit a new claim
        messagebox.showinfo("Info", "Please use the Recovered Items section to submit a claim for a specific item.")
    
    def load_requests(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get filtered requests
        status_filter = None if self.status_var.get() == "All" else self.status_var.get()
        requests = get_claim_requests(self.controller.db_path, status_filter)
        
        # Add items to treeview
        for req in requests:
            self.tree.insert("", tk.END, values=(
                req["id"],
                req["student_id"],
                req["student_name"],
                req["item_name"],
                req["requested_by"],
                req["date_requested"],
                req["status"]
            ))
    
    def approve_request(self):
        # Get selected request
        try:
            selected = self.tree.selection()[0]
            request_id = self.tree.item(selected, "values")[0]
            
            # Confirm action
            if messagebox.askyesno("Confirm", "Are you sure you want to approve this claim?"):
                # Approve the claim
                success = approve_claim(
                    self.controller.db_path,
                    request_id,
                    self.controller.current_user
                )
                
                if success:
                    messagebox.showinfo("Success", "Claim approved successfully")
                    self.load_requests()  # Refresh the list
        except IndexError:
            messagebox.showerror("Error", "Please select a request")
    
    def reject_request(self):
        # Get selected request
        try:
            selected = self.tree.selection()[0]
            request_id = self.tree.item(selected, "values")[0]
            
            # Confirm action
            if messagebox.askyesno("Confirm", "Are you sure you want to reject this claim?"):
                # TODO: Implement reject claim functionality
                messagebox.showinfo("Success", "Claim rejected successfully")
                self.load_requests()  # Refresh the list
        except IndexError:
            messagebox.showerror("Error", "Please select a request")
