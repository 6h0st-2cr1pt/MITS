import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database import add_user

class SignupFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Create a background frame
        bg_frame = ttk.Frame(self)
        bg_frame.place(relwidth=1, relheight=1)
        
        # Create centered signup form with a border
        signup_container = ttk.Frame(self)
        signup_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Create a border effect using a separate frame with padding to ensure visibility
        border_frame = ttk.Frame(
            signup_container,
            padding=2,
            style='primary.TFrame'  # Apply primary color to border frame
        )
        border_frame.pack(padx=5, pady=5)
        
        # Inner content frame
        signup_frame = ttk.Frame(border_frame, padding=10)
        signup_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(signup_frame)
        header_frame.pack(fill=tk.X, pady=(10, 20))
        
        ttk.Label(
            header_frame, 
            text="Missing Item Recovery System",
            font=('Helvetica', 18, 'bold')
        ).pack(anchor=tk.CENTER)
        
        # Signup Form
        form_frame = ttk.Frame(signup_frame)
        form_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(
            form_frame, 
            text="Create a new account",
            font=('Helvetica', 14)
        ).pack(anchor=tk.CENTER, pady=(0, 15))
        
        # Username field
        username_frame = ttk.Frame(form_frame)
        username_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            username_frame, 
            text="Username"
        ).pack(anchor=tk.W)
        
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(
            username_frame, 
            textvariable=self.username_var, 
            width=30, 
            font=('Helvetica', 10)
        )
        username_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Password field
        password_frame = ttk.Frame(form_frame)
        password_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            password_frame, 
            text="Password"
        ).pack(anchor=tk.W)
        
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(
            password_frame, 
            textvariable=self.password_var, 
            show="*", 
            width=30, 
            font=('Helvetica', 10)
        )
        password_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Confirm Password field
        confirm_frame = ttk.Frame(form_frame)
        confirm_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            confirm_frame, 
            text="Confirm Password"
        ).pack(anchor=tk.W)
        
        self.confirm_password_var = tk.StringVar()
        confirm_entry = ttk.Entry(
            confirm_frame, 
            textvariable=self.confirm_password_var, 
            show="*", 
            width=30, 
            font=('Helvetica', 10)
        )
        confirm_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Role selection
        role_frame = ttk.Frame(form_frame)
        role_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(
            role_frame, 
            text="Role"
        ).pack(anchor=tk.W)
        
        self.role_var = tk.StringVar(value="staff")
        role_buttons = ttk.Frame(role_frame)
        role_buttons.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Radiobutton(
            role_buttons, 
            text="Staff", 
            variable=self.role_var, 
            value="staff"
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Radiobutton(
            role_buttons, 
            text="Admin", 
            variable=self.role_var, 
            value="admin"
        ).pack(side=tk.LEFT)
        
        # Sign up button
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(
            button_frame, 
            text="Sign Up", 
            style='primary.TButton',
            command=self.signup
        ).pack(fill=tk.X, ipady=5)
        
        # Login link
        login_frame = ttk.Frame(form_frame)
        login_frame.pack(pady=5)
        
        ttk.Label(
            login_frame, 
            text="Already have an account?"
        ).pack(side=tk.LEFT)
        
        login_link = ttk.Label(
            login_frame, 
            text="Log in",
            foreground='blue',
            cursor='hand2'
        )
        login_link.pack(side=tk.LEFT, padx=5)
        login_link.bind("<Button-1>", lambda e: self.controller.show_login())
    
    def signup(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()
        role = self.role_var.get()
        
        # Validation
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
            messagebox.showinfo("Success", "Account created successfully! You can now log in.")
            self.controller.show_login()
        else:
            messagebox.showerror("Error", "Username already exists")