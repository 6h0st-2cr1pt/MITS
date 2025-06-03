import os
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3
from PIL import Image, ImageTk
import time
import threading

# Import our modules
from splash_screen import SplashScreen
from login import LoginFrame
from signup import SignupFrame
from dashboard import Dashboard
from database import setup_database

class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title("Missing Item Recovery System")
        self.geometry("1200x720")
        self.resizable(True, True)
        self.minsize(1000, 600)

        # Initialize database
        self.db_path = "item_recovery.db"
        setup_database(self.db_path)

        # Set default theme
        self.set_theme("darkly")

        # Initialize ttk style
        self.ttk_style = ttk.Style()

        # Configure styles to avoid text highlighting
        self.configure_styles()

        # Initialize variables
        self.current_user = None
        self.user_role = None

        # Create a container frame to hold all frames
        self.container = ttk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)

        # Dictionary to hold frames
        self.frames = {}

        # Start with splash screen
        self.show_splash_screen()

    def configure_styles(self):
        """Configure custom styles to optimize UI appearance"""
        # Configure button styles
        self.ttk_style.configure('TButton', font=('Helvetica', 10))
        self.ttk_style.configure('primary.TButton', font=('Helvetica', 10))
        self.ttk_style.configure('success.TButton', font=('Helvetica', 10))
        self.ttk_style.configure('info.TButton', font=('Helvetica', 10))
        self.ttk_style.configure('warning.TButton', font=('Helvetica', 10))
        self.ttk_style.configure('danger.TButton', font=('Helvetica', 10))

        # Configure label styles
        self.ttk_style.configure('TLabel', font=('Helvetica', 10))
        self.ttk_style.configure('inverse.TLabel', foreground='white', background=self.ttk_style.colors.secondary)

        # Configure treeview
        self.ttk_style.configure('Treeview', rowheight=25, font=('Helvetica', 10))
        self.ttk_style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'))

        # Configure entry fields
        self.ttk_style.configure('TEntry', font=('Helvetica', 10))

        # Configure frames
        self.ttk_style.configure('TFrame', background=self.ttk_style.colors.bg)
        self.ttk_style.configure('secondary.TFrame', background=self.ttk_style.colors.secondary)

    def show_splash_screen(self):
        # Clear the container
        for widget in self.container.winfo_children():
            widget.destroy()

        # Show splash screen - we don't pack it here since it packs itself
        splash = SplashScreen(self)
        # No need to call pack() as the SplashScreen now handles its own layout

    def show_login(self):
        # Clear the container
        for widget in self.container.winfo_children():
            widget.destroy()

        # Create login frame
        login_frame = LoginFrame(self.container, self)
        login_frame.pack(fill=tk.BOTH, expand=True)
        self.frames["login"] = login_frame

    def show_signup(self):
        # Clear the container
        for widget in self.container.winfo_children():
            widget.destroy()

        # Create signup frame
        signup_frame = SignupFrame(self.container, self)
        signup_frame.pack(fill=tk.BOTH, expand=True)
        self.frames["signup"] = signup_frame

    def login_success(self, username, role):
        # Set current user and role
        self.current_user = username
        self.user_role = role

        # Show dashboard
        self.show_dashboard()

    def show_dashboard(self):
        # Clear the container
        for widget in self.container.winfo_children():
            widget.destroy()

        # Create dashboard
        dashboard = Dashboard(self.container, self)
        dashboard.pack(fill=tk.BOTH, expand=True)
        self.frames["dashboard"] = dashboard

    def logout(self):
        # Clear user data
        self.current_user = None
        self.user_role = None

        # Show login screen
        self.show_login()

    def set_theme(self, theme_name):
        # Change application theme
        self.ttk_style = ttk.Style(theme_name)
        # Reconfigure styles after theme change
        self.configure_styles()

if __name__ == "__main__":
    app = App()
    app.mainloop()