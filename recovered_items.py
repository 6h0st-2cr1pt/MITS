import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os
import shutil
from datetime import datetime
from database import add_recovered_item, get_recovered_items, submit_claim_request

class RecoveredItemsFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Create images directory if it doesn't exist
        os.makedirs("images", exist_ok=True)
        
        # Title and search area
        self.create_header()
        
        # Main content split into two panes
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left side - Items list
        self.create_items_list(paned)
        
        # Right side - Item details/form
        self.create_item_form(paned)
        
        # Selected item image
        self.selected_image_path = None
        
        # Load initial data
        self.load_items()
    
    def create_header(self):
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        ttk.Label(
            header_frame, 
            text="Recovered Items",
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
        columns = ("id", "item_name", "color", "date_found", "status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=20)
        
        # Configure columns
        self.tree.heading("id", text="ID")
        self.tree.heading("item_name", text="Item Name")
        self.tree.heading("color", text="Color")
        self.tree.heading("date_found", text="Date Found")
        self.tree.heading("status", text="Status")
        
        self.tree.column("id", width=50)
        self.tree.column("item_name", width=150)
        self.tree.column("color", width=100)
        self.tree.column("date_found", width=150)
        self.tree.column("status", width=100)
        
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack items
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Detail view frame
        detail_frame = ttk.Frame(list_frame, padding=10)
        detail_frame.pack(fill=tk.BOTH, pady=10)
        
        # Item details
        self.detail_label = ttk.Label(
            detail_frame, 
            text="Select an item to view details",
            wraplength=400
        )
        self.detail_label.pack(pady=5)
        
        # Image preview
        self.image_label = ttk.Label(detail_frame)
        self.image_label.pack(pady=5)
        
        # Claim button (only visible for staff)
        if self.controller.user_role == "staff":
            self.claim_button = ttk.Button(
                detail_frame,
                text="Request Claim",
                style='info.TButton',
                command=self.request_claim,
                state=tk.DISABLED
            )
            self.claim_button.pack(pady=5)
    
    def create_item_form(self, parent):
        form_frame = ttk.Frame(parent, padding=10)
        parent.add(form_frame, weight=1)
        
        # Form title
        ttk.Label(
            form_frame, 
            text="Register Found Item",
            font=('Helvetica', 16, 'bold')
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Form fields
        fields_frame = ttk.Frame(form_frame)
        fields_frame.pack(fill=tk.BOTH, expand=True)
        
        # Item Name
        ttk.Label(fields_frame, text="Item Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.item_name_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=self.item_name_var, width=30).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Color
        ttk.Label(fields_frame, text="Color:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.color_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=self.color_var, width=30).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Location Found
        ttk.Label(fields_frame, text="Location Found:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.location_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=self.location_var, width=30).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Description
        ttk.Label(fields_frame, text="Description:").grid(row=3, column=0, sticky=tk.NW, pady=5)
        self.description_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=self.description_var, width=30).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Image
        ttk.Label(fields_frame, text="Image:").grid(row=4, column=0, sticky=tk.W, pady=5)
        image_button_frame = ttk.Frame(fields_frame)
        image_button_frame.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        self.image_path_var = tk.StringVar()
        ttk.Label(
            image_button_frame, 
            textvariable=self.image_path_var,
            wraplength=200
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            image_button_frame,
            text="Browse...",
            style='info.TButton',
            command=self.browse_image
        ).pack(side=tk.LEFT, padx=5)
        
        # Preview image
        self.preview_frame = ttk.Frame(fields_frame)
        self.preview_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.preview_label = ttk.Label(self.preview_frame)
        self.preview_label.pack()
        
        # Button frame
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            button_frame,
            text="Register Item",
            style='success.TButton',
            command=self.register_item
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
        items = get_recovered_items(self.controller.db_path, self.search_var.get())
        
        # Add items to treeview
        for item in items:
            self.tree.insert("", tk.END, values=(
                item["id"],
                item["item_name"],
                item["color"],
                item["date_found"],
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
            selected = self.tree.selection()[0]
            item_values = self.tree.item(selected, "values")
            
            # Get full item data from database
            items = get_recovered_items(self.controller.db_path)
            item = next((i for i in items if str(i["id"]) == str(item_values[0])), None)
            
            if item:
                # Update detail label
                detail_text = f"Item: {item['item_name']}\n"
                detail_text += f"Description: {item['description']}\n"
                detail_text += f"Color: {item['color']}\n"
                detail_text += f"Found at: {item['location_found']}\n"
                detail_text += f"Found by: {item['found_by']}\n"
                detail_text += f"Date: {item['date_found']}\n"
                detail_text += f"Status: {item['status']}"
                
                self.detail_label.config(text=detail_text)
                
                # Display image if available
                if item["image_path"] and os.path.exists(item["image_path"]):
                    self.display_image(item["image_path"], self.image_label)
                else:
                    self.image_label.config(image="")
                
                # Enable claim button if item is available
                if hasattr(self, 'claim_button'):
                    if item["status"] == "Available":
                        self.claim_button.config(state=tk.NORMAL)
                        # Store the selected item ID for claim request
                        self.selected_item_id = item["id"]
                    else:
                        self.claim_button.config(state=tk.DISABLED)
            
        except (IndexError, StopIteration):
            self.detail_label.config(text="Select an item to view details")
            self.image_label.config(image="")
            if hasattr(self, 'claim_button'):
                self.claim_button.config(state=tk.DISABLED)
    
    def browse_image(self):
        file_path = filedialog.askopenfilename(
            initialdir="/",
            title="Select Image",
            filetypes=(("Image files", "*.jpg *.jpeg *.png *.gif"), ("All files", "*.*"))
        )
        
        if file_path:
            self.image_path_var.set(os.path.basename(file_path))
            self.selected_image_path = file_path
            self.display_image(file_path, self.preview_label)
    
    def display_image(self, file_path, label_widget):
        try:
            # Open and resize image
            img = Image.open(file_path)
            img = img.resize((200, 200), Image.LANCZOS)
            
            # Convert to PhotoImage
            photo_img = ImageTk.PhotoImage(img)
            
            # Update label
            label_widget.config(image=photo_img)
            label_widget.image = photo_img  # Keep a reference
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {str(e)}")
    
    def register_item(self):
        # Get form data
        item_name = self.item_name_var.get().strip()
        color = self.color_var.get().strip()
        location = self.location_var.get().strip()
        description = self.description_var.get().strip()
        
        # Validate form
        if not item_name:
            messagebox.showerror("Error", "Item Name is required")
            return
        
        # Process image if selected
        image_path = None
        if self.selected_image_path:
            # Create a timestamped filename
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{timestamp}_{os.path.basename(self.selected_image_path)}"
            destination = os.path.join("images", filename)
            
            # Copy image to images directory
            try:
                shutil.copy2(self.selected_image_path, destination)
                image_path = destination
            except Exception as e:
                messagebox.showerror("Error", f"Failed to copy image: {str(e)}")
                return
        
        # Add item to database
        success = add_recovered_item(
            self.controller.db_path,
            self.controller.current_user,
            item_name,
            description,
            color,
            location,
            image_path
        )
        
        if success:
            messagebox.showinfo("Success", "Found item registered successfully")
            self.clear_form()
            self.load_items()
    
    def request_claim(self):
        # Open dialog to get student info
        claim_dialog = ttk.Toplevel(self)
        claim_dialog.title("Request Item Claim")
        claim_dialog.geometry("400x200")
        claim_dialog.resizable(False, False)
        
        # Student ID
        ttk.Label(claim_dialog, text="Student ID:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        student_id_var = tk.StringVar()
        ttk.Entry(claim_dialog, textvariable=student_id_var, width=30).grid(row=0, column=1, padx=10, pady=10)
        
        # Student Name
        ttk.Label(claim_dialog, text="Student Name:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        student_name_var = tk.StringVar()
        ttk.Entry(claim_dialog, textvariable=student_name_var, width=30).grid(row=1, column=1, padx=10, pady=10)
        
        # Buttons
        button_frame = ttk.Frame(claim_dialog)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            button_frame,
            text="Submit",
            style='success.TButton',
            command=lambda: self.submit_claim(
                student_id_var.get().strip(),
                student_name_var.get().strip(),
                claim_dialog
            )
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancel",
            style='secondary.TButton',
            command=claim_dialog.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def submit_claim(self, student_id, student_name, dialog):
        # Validate input
        if not student_id or not student_name:
            messagebox.showerror("Error", "Student ID and Name are required", parent=dialog)
            return
        
        # Submit claim request
        success = submit_claim_request(
            self.controller.db_path,
            student_id,
            student_name,
            self.selected_item_id,
            self.controller.current_user
        )
        
        if success:
            messagebox.showinfo("Success", "Claim request submitted successfully", parent=dialog)
            dialog.destroy()
            self.load_items()  # Refresh the list
    
    def clear_form(self):
        self.item_name_var.set("")
        self.color_var.set("")
        self.location_var.set("")
        self.description_var.set("")
        self.image_path_var.set("")
        self.selected_image_path = None
        self.preview_label.config(image="")
