import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database import get_user_list, add_user

class UserManagementFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Role-based access control
        if self.controller.user_role != "admin":
            self.create_access_denied()
            return
        
        # Title
        self.create_header()
        
        # Main content split into panes
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left side - Users list
        self.create_users_list(paned)
        
        # Right side - Add user form
        self.create_user_form(paned)
        
        # Load initial data
        self.load_users()
    
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
            text="Only administrators can access user management.",
            font=('Helvetica', 12)
        ).pack()
    
    def create_header(self):
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        ttk.Label(
            header_frame, 
            text="User Management",
            font=('Helvetica', 20, 'bold')
        ).pack(side=tk.LEFT)
    
    def create_users_list(self, parent):
        list_frame = ttk.Frame(parent)
        parent.add(list_frame, weight=2)
        
        # Users list with scrollbar
        columns = ("id", "username", "role", "created_at")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=20)
        
        # Configure columns
        self.tree.heading("id", text="ID")
        self.tree.heading("username", text="Username")
        self.tree.heading("role", text="Role")
        self.tree.heading("created_at", text="Created At")
        
        self.tree.column("id", width=50)
        self.tree.column("username", width=150)
        self.tree.column("role", width=100)
        self.tree.column("created_at", width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack items
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_user_form(self, parent):
        form_frame = ttk.Frame(parent, padding=10)
        parent.add(form_frame, weight=1)
        
        # Form title
        ttk.Label(
            form_frame, 
            text="Add New User",
            font=('Helvetica', 16, 'bold')
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Form fields
        fields_frame = ttk.Frame(form_frame)
        fields_frame.pack(fill=tk.BOTH, expand=True)
        
        # Username
        ttk.Label(fields_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=self.username_var, width=30).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Password
        ttk.Label(fields_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=self.password_var, show="*", width=30).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Confirm Password
        ttk.Label(fields_frame, text="Confirm Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.confirm_password_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=self.confirm_password_var, show="*", width=30).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Role
        ttk.Label(fields_frame, text="Role:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.role_var = tk.StringVar(value="staff")
        
        role_frame = ttk.Frame(fields_frame)
        role_frame.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(
            role_frame, 
            text="Staff", 
            variable=self.role_var, 
            value="staff"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Radiobutton(
            role_frame, 
            text="Admin", 
            variable=self.role_var, 
            value="admin"
        ).pack(side=tk.LEFT)
        
        # Button frame
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            button_frame,
            text="Add User",
            style='success.TButton',
            command=self.add_user
        ).pack(side=tk.RIGHT)
        
        ttk.Button(
            button_frame,
            text="Clear Form",
            style='secondary.TButton',
            command=self.clear_form
        ).pack(side=tk.RIGHT, padx=5)
    
    def load_users(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get users from database
        users = get_user_list(self.controller.db_path)
        
        # Add items to treeview
        for user in users:
            self.tree.insert("", tk.END, values=(
                user["id"],
                user["username"],
                user["role"],
                user["created_at"]
            ))
    
    def add_user(self):
        # Get form data
        username = self.username_var.get().strip()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()
        role = self.role_var.get()
        
        # Validate form
        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        # Add user to database
        success = add_user(self.controller.db_path, username, password, role)
        
        if success:
            messagebox.showinfo("Success", "User added successfully")
            self.clear_form()
            self.load_users()
        else:
            messagebox.showerror("Error", "Username already exists")
    
    def clear_form(self):
        self.username_var.set("")
        self.password_var.set("")
        self.confirm_password_var.set("")
        self.role_var.set("staff")
