import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

class SplashScreen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Configure to fill the entire window
        self.pack(fill=tk.BOTH, expand=True)
        
        # Create a container with primary background color
        self.configure(bootstyle="primary")
        
        # Create a content frame for the splash screen centered in the window
        content_frame = ttk.Frame(self, bootstyle="primary")
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create a border frame with padding
        border_frame = ttk.Frame(content_frame, padding=20, bootstyle="primary")
        border_frame.pack(padx=20, pady=20)

        # Top separator
        ttk.Separator(border_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(0, 20))

        # Logo or app name
        logo_label = ttk.Label(
            border_frame,
            text="Missing Item Recovery System",
            font=('Helvetica', 28, 'bold'),
            bootstyle="inverse-primary"
        )
        logo_label.pack(pady=20)

        # Progress bar
        self.progress = ttk.Progressbar(
            border_frame,
            mode='determinate',
            length=400,
            bootstyle="primary-striped"
        )
        self.progress.pack(pady=20)
        self.progress['value'] = 0

        # Version label
        version_label = ttk.Label(
            border_frame,
            text="Version 1.0",
            font=('Helvetica', 10),
            bootstyle="inverse-primary"
        )
        version_label.pack(pady=10)

        # Loading message
        self.loading_label = ttk.Label(
            border_frame,
            text="Loading...",
            font=('Helvetica', 12),
            bootstyle="inverse-primary"
        )
        self.loading_label.pack(pady=10)

        # Bottom separator
        ttk.Separator(border_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(20, 0))

        # Copyright
        copyright_label = ttk.Label(
            border_frame,
            text="© 2023 Missing Item Recovery System",
            font=('Helvetica', 8),
            bootstyle="inverse-primary"
        )
        copyright_label.pack(pady=20)

        # Start the loading sequence
        self.start_loading_sequence()

    def start_loading_sequence(self):
        """Start the loading sequence with progress updates"""
        self.update_progress(0, "Initializing components...")
        self.after(500, lambda: self.update_progress(20, "Loading database..."))
        self.after(1000, lambda: self.update_progress(40, "Preparing UI..."))
        self.after(1500, lambda: self.update_progress(60, "Loading modules..."))
        self.after(2000, lambda: self.update_progress(80, "Almost ready..."))
        self.after(2500, lambda: self.update_progress(100, "Complete!"))
        # Add a small delay before transitioning to login and properly cleaning up
        self.after(3000, self.finish_splash)
    
    def finish_splash(self):
        """Properly remove splash screen and transition to login"""
        # Destroy the splash screen frame
        self.destroy()
        # Show login screen
        self.parent.show_login()

    def update_progress(self, value, message):
        """Update progress bar and message"""
        self.progress['value'] = value
        self.loading_label.config(text=message)