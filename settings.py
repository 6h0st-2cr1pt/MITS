import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import os
import json

class SettingsFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Available themes
        self.themes = ['darkly', 'solar', 'superhero', 'cyborg', 'vapor']
        
        # Settings file path
        self.settings_file = "settings.json"
        
        # Load settings
        self.load_settings()
        
        # Create settings content
        self.create_settings()
    
    def load_settings(self):
        """Load settings from file or create default settings"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    self.settings = json.load(f)
            except:
                self.settings = self.get_default_settings()
        else:
            self.settings = self.get_default_settings()
    
    def get_default_settings(self):
        """Return default settings"""
        return {
            "theme": "darkly",
            "startup_maximized": False,
            "confirm_logout": True,
            "auto_refresh": True,
            "refresh_interval": 60  # seconds
        }
    
    def save_settings(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
            return False
    
    def create_settings(self):
        # Main container with scrollbar
        container = ttk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create a canvas with scrollbar
        canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        # Scrollable frame
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Settings title
        ttk.Label(
            scrollable_frame, 
            text="Settings",
            font=('Helvetica', 24, 'bold')
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # Theme settings
        self.create_theme_settings(scrollable_frame)
        
        # Application settings
        self.create_application_settings(scrollable_frame)
        
        # About section
        self.create_about_section(scrollable_frame)
        
        # Save button
        save_button = ttk.Button(
            scrollable_frame,
            text="Save Settings",
            style='success.TButton',
            command=self.save_all_settings
        )
        save_button.pack(anchor=tk.CENTER, pady=20)
    
    def create_theme_settings(self, parent):
        theme_frame = ttk.LabelFrame(parent, text="Application Theme", padding=15)
        theme_frame.pack(fill=tk.X, pady=10)
        
        # Current theme
        current_theme = ttk.Frame(theme_frame)
        current_theme.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            current_theme, 
            text="Current Theme:",
            font=('Helvetica', 12)
        ).pack(side=tk.LEFT)
        
        ttk.Label(
            current_theme, 
            text=self.controller.style.theme.name.capitalize(),
            font=('Helvetica', 12, 'bold')
        ).pack(side=tk.LEFT, padx=5)
        
        # Theme selection
        ttk.Label(
            theme_frame, 
            text="Select Theme:",
            font=('Helvetica', 12)
        ).pack(anchor=tk.W, pady=(10, 5))
        
        # Theme grid
        theme_grid = ttk.Frame(theme_frame)
        theme_grid.pack(fill=tk.X, pady=5)
        
        # Theme buttons with preview
        self.theme_buttons = []
        for i, theme in enumerate(self.themes):
            theme_card = ttk.Frame(theme_grid, padding=5)
            theme_card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky=tk.W)
            
            # Theme preview (colored rectangle)
            preview_colors = {
                'darkly': '#375a7f',
                'solar': '#b58900',
                'superhero': '#4c9be8',
                'cyborg': '#2a9fd6',
                'vapor': '#ff00ff'
            }
            
            preview = tk.Canvas(
                theme_card, 
                width=80, 
                height=40, 
                bg=preview_colors.get(theme, '#375a7f'),
                highlightthickness=1,
                highlightbackground="gray"
            )
            preview.pack(pady=(0, 5))
            
            # Theme name
            ttk.Label(
                theme_card,
                text=theme.capitalize(),
                font=('Helvetica', 10)
            ).pack()
            
            # Select button
            is_current = theme == self.controller.style.theme.name
            btn = ttk.Button(
                theme_card,
                text="Selected" if is_current else "Select",
                style='success.TButton' if is_current else 'outline.TButton',
                width=10,
                command=lambda t=theme: self.change_theme(t)
            )
            btn.pack(pady=5)
            self.theme_buttons.append((theme, btn))
        
        # Apply theme at startup
        startup_theme_frame = ttk.Frame(theme_frame)
        startup_theme_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            startup_theme_frame,
            text="Apply selected theme at startup:",
            font=('Helvetica', 11)
        ).pack(side=tk.LEFT)
        
        self.startup_theme_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            startup_theme_frame,
            variable=self.startup_theme_var
        ).pack(side=tk.LEFT, padx=5)
    
    def create_application_settings(self, parent):
        app_frame = ttk.LabelFrame(parent, text="Application Settings", padding=15)
        app_frame.pack(fill=tk.X, pady=10)
        
        # Start maximized
        max_frame = ttk.Frame(app_frame)
        max_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            max_frame,
            text="Start application maximized:",
            font=('Helvetica', 11)
        ).pack(side=tk.LEFT)
        
        self.maximized_var = tk.BooleanVar(value=self.settings.get("startup_maximized", False))
        ttk.Checkbutton(
            max_frame,
            variable=self.maximized_var
        ).pack(side=tk.LEFT, padx=5)
        
        # Confirm logout
        logout_frame = ttk.Frame(app_frame)
        logout_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            logout_frame,
            text="Confirm before logout:",
            font=('Helvetica', 11)
        ).pack(side=tk.LEFT)
        
        self.confirm_logout_var = tk.BooleanVar(value=self.settings.get("confirm_logout", True))
        ttk.Checkbutton(
            logout_frame,
            variable=self.confirm_logout_var
        ).pack(side=tk.LEFT, padx=5)
        
        # Auto refresh
        refresh_frame = ttk.Frame(app_frame)
        refresh_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            refresh_frame,
            text="Auto refresh data:",
            font=('Helvetica', 11)
        ).pack(side=tk.LEFT)
        
        self.auto_refresh_var = tk.BooleanVar(value=self.settings.get("auto_refresh", True))
        ttk.Checkbutton(
            refresh_frame,
            variable=self.auto_refresh_var,
            command=self.toggle_refresh_interval
        ).pack(side=tk.LEFT, padx=5)
        
        # Refresh interval
        interval_frame = ttk.Frame(app_frame)
        interval_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            interval_frame,
            text="Refresh interval (seconds):",
            font=('Helvetica', 11)
        ).pack(side=tk.LEFT)
        
        self.interval_var = tk.StringVar(value=str(self.settings.get("refresh_interval", 60)))
        self.interval_spinbox = ttk.Spinbox(
            interval_frame,
            from_=10,
            to=300,
            increment=10,
            textvariable=self.interval_var,
            width=5,
            state="normal" if self.auto_refresh_var.get() else "disabled"
        )
        self.interval_spinbox.pack(side=tk.LEFT, padx=5)
    
    def create_about_section(self, parent):
        about_frame = ttk.LabelFrame(parent, text="About", padding=15)
        about_frame.pack(fill=tk.X, pady=10)
        
        # App logo/icon (placeholder)
        logo_frame = ttk.Frame(about_frame)
        logo_frame.pack(anchor=tk.CENTER, pady=10)
        
        # App name and version
        ttk.Label(
            about_frame, 
            text="Missing Item Recovery System",
            font=('Helvetica', 16, 'bold')
        ).pack(anchor=tk.CENTER)
        
        ttk.Label(
            about_frame, 
            text="Version 2.0",
            font=('Helvetica', 12)
        ).pack(anchor=tk.CENTER, pady=5)
        
        # Description
        ttk.Label(
            about_frame, 
            text="An offline desktop software designed to help staff track missing and recovered items. "
                 "The system allows students to report missing items and claim lost property, "
                 "with a reward system for honest students.",
            wraplength=600,
            justify=tk.CENTER
        ).pack(anchor=tk.CENTER, pady=10)
        
        # Features
        features_frame = ttk.Frame(about_frame)
        features_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            features_frame,
            text="Key Features:",
            font=('Helvetica', 12, 'bold')
        ).pack(anchor=tk.W)
        
        features = [
            "User management with role-based access",
            "Missing item tracking and reporting",
            "Found item registration with image support",
            "Claim request and verification system",
            "Student reward system for honesty",
            "Customizable themes and settings"
        ]
        
        for feature in features:
            ttk.Label(
                features_frame,
                text=f"• {feature}"
            ).pack(anchor=tk.W, padx=20)
        
        # Copyright
        ttk.Label(
            about_frame, 
            text="© 2025 Missing Item Recovery System",
            font=('Helvetica', 10)
        ).pack(anchor=tk.CENTER, pady=10)
    
    def toggle_refresh_interval(self):
        """Enable/disable refresh interval based on auto refresh setting"""
        if self.auto_refresh_var.get():
            self.interval_spinbox.config(state="normal")
        else:
            self.interval_spinbox.config(state="disabled")
    
    def change_theme(self, theme_name):
        # Apply the new theme
        self.controller.set_theme(theme_name)
        
        # Update settings
        self.settings["theme"] = theme_name
        
        # Update button states
        for theme, button in self.theme_buttons:
            if theme == theme_name:
                button.config(text="Selected", style='success.TButton')
            else:
                button.config(text="Select", style='outline.TButton')
        
        # Show confirmation
        messagebox.showinfo("Theme Changed", f"The application theme has been changed to {theme_name.capitalize()}")
    
    def save_all_settings(self):
        """Save all settings"""
        # Update settings from UI
        self.settings["theme"] = self.controller.style.theme.name
        self.settings["startup_maximized"] = self.maximized_var.get()
        self.settings["confirm_logout"] = self.confirm_logout_var.get()
        self.settings["auto_refresh"] = self.auto_refresh_var.get()
        
        try:
            self.settings["refresh_interval"] = int(self.interval_var.get())
        except ValueError:
            self.settings["refresh_interval"] = 60
        
        # Save to file
        if self.save_settings():
            messagebox.showinfo("Success", "Settings saved successfully")
    
    def apply_settings(self):
        """Apply settings to the application"""
        # Apply theme
        if self.settings.get("theme"):
            self.controller.set_theme(self.settings["theme"])
        
        # Apply other settings as needed
        # This would be called from the main application when loading
        pass
