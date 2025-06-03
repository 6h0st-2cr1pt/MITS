import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database import verify_login

class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Create a background frame
        bg_frame = ttk.Frame(self)
        bg_frame.place(relwidth=1, relheight=1)
        
        # Create centered login form with a border
        login_container = ttk.Frame(self)
        login_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Create a border effect using a separate frame with padding to ensure visibility
        border_frame = ttk.Frame(
            login_container,
            padding=2,
            style='primary.TFrame'  # Apply primary color to border frame
        )
        border_frame.pack(padx=5, pady=5)
        
        # Inner content frame
        login_frame = ttk.Frame(border_frame, padding=10)
        login_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(login_frame)
        header_frame.pack(fill=tk.X, pady=(10, 20))
        
        ttk.Label(
            header_frame, 
            text="Missing Item Recovery System",
            font=('Helvetica', 18, 'bold')
        ).pack(anchor=tk.CENTER)
        
        # Login Form
        form_frame = ttk.Frame(login_frame)
        form_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(
            form_frame, 
            text="Log in to your account",
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
        password_frame.pack(fill=tk.X, pady=(0, 15))
        
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
        
        # Login button
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(
            button_frame, 
            text="Login", 
            style='primary.TButton',
            command=self.login
        ).pack(fill=tk.X, ipady=5)
        
        # Sign up link
        signup_frame = ttk.Frame(form_frame)
        signup_frame.pack(pady=5)
        
        ttk.Label(
            signup_frame, 
            text="Don't have an account?"
        ).pack(side=tk.LEFT)
        
        signup_link = ttk.Label(
            signup_frame, 
            text="Sign up",
            foreground='blue',
            cursor='hand2'
        )
        signup_link.pack(side=tk.LEFT, padx=5)
        signup_link.bind("<Button-1>", lambda e: self.controller.show_signup())
        
        # Version label
        ttk.Label(
            login_frame, 
            text="Version 2.0",
            font=('Helvetica', 8)
        ).pack(side=tk.BOTTOM, pady=5)
    
    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Verify login credentials
        success, role = verify_login(self.controller.db_path, username, password)
        
        if success:
            # Login successful
            self.controller.login_success(username, role)
        else:
            # Login failed
            messagebox.showerror("Login Failed", "Invalid username or password")