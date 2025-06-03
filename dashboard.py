import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import shutil
from datetime import datetime

# Import our modules
from missing_items import MissingItemsFrame
from recovered_items import RecoveredItemsFrame
from rewards import RewardsFrame
from claim_requests import ClaimRequestsFrame
from user_management import UserManagementFrame
from settings import SettingsFrame

class Dashboard(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar and content area
        self.create_sidebar()
        self.create_content_area()
        
        # Default to showing appropriate frame based on role
        self.show_frame(self.default_frame)
    
    def create_sidebar(self):
        # Create the sidebar frame
        sidebar = ttk.Frame(self.main_container, style='secondary.TFrame', padding=10)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        # App title
        ttk.Label(
            sidebar, 
            text="Item Recovery",
            font=('Helvetica', 16, 'bold'),
            style='inverse.TLabel'
        ).pack(pady=(0, 20))
        
        # User info
        user_frame = ttk.Frame(sidebar, style='secondary.TFrame')
        user_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            user_frame, 
            text=f"Logged in as:",
            font=('Helvetica', 10),
            style='inverse.TLabel'
        ).pack(anchor=tk.W)
        
        ttk.Label(
            user_frame, 
            text=f"{self.controller.current_user} ({self.controller.user_role.capitalize()})",
            font=('Helvetica', 12, 'bold'),
            style='inverse.TLabel'
        ).pack(anchor=tk.W)
        
        # Navigation buttons - only show appropriate options based on role
        if self.controller.user_role == "admin":
            # Admin-only options
            self.create_sidebar_button(sidebar, "User Management", lambda: self.show_frame("user_management"))
            self.create_sidebar_button(sidebar, "Rewards", lambda: self.show_frame("rewards"))
            self.create_sidebar_button(sidebar, "Claim Requests", lambda: self.show_frame("claim_requests"))
        elif self.controller.user_role == "staff":
            # Staff-only options
            self.create_sidebar_button(sidebar, "Missing Items", lambda: self.show_frame("missing_items"))
            self.create_sidebar_button(sidebar, "Recovered Items", lambda: self.show_frame("recovered_items"))
            self.create_sidebar_button(sidebar, "Claim Requests", lambda: self.show_frame("claim_requests"))
        
        # Settings available to all users
        self.create_sidebar_button(sidebar, "Settings", lambda: self.show_frame("settings"))
        
        # Logout button at the bottom
        ttk.Separator(sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        self.create_sidebar_button(sidebar, "Logout", self.logout, style='danger.TButton')
    
    def create_sidebar_button(self, parent, text, command, style='primary.Outline.TButton'):
        btn = ttk.Button(
            parent,
            text=text,
            command=command,
            style=style,
            width=20
        )
        btn.pack(pady=5, fill=tk.X)
        return btn
    
    def create_content_area(self):
        # Create the content frame
        self.content_frame = ttk.Frame(self.main_container, padding=10)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Dictionary to hold different frames
        self.frames = {}
        
        # Create frames based on user role
        if self.controller.user_role == "admin":
            # Admin-only frames
            self.frames["user_management"] = UserManagementFrame(self.content_frame, self.controller)
            self.frames["rewards"] = RewardsFrame(self.content_frame, self.controller)
            self.frames["claim_requests"] = ClaimRequestsFrame(self.content_frame, self.controller)
            
            # Set default frame for admin
            self.default_frame = "user_management"
        elif self.controller.user_role == "staff":
            # Staff-only frames
            self.frames["missing_items"] = MissingItemsFrame(self.content_frame, self.controller)
            self.frames["recovered_items"] = RecoveredItemsFrame(self.content_frame, self.controller)
            self.frames["claim_requests"] = ClaimRequestsFrame(self.content_frame, self.controller)
            
            # Set default frame for staff
            self.default_frame = "missing_items"
        
        # Settings frame for all users
        self.frames["settings"] = SettingsFrame(self.content_frame, self.controller)
    
    def show_frame(self, frame_name):
        # Check if the frame exists (role-based access control)
        if frame_name not in self.frames:
            messagebox.showerror("Access Denied", "You don't have permission to access this feature.")
            return
            
        # Hide all frames
        for frame in self.frames.values():
            frame.pack_forget()
        
        # Show the selected frame
        self.frames[frame_name].pack(fill=tk.BOTH, expand=True)
    
    def logout(self):
        # Confirm logout
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.controller.logout()
