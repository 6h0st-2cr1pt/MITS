import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database import add_reward, verify_reward, get_rewards, get_recovered_items

class RewardsFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Title and filters
        self.create_header()
        
        # Main content split into panes
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left side - Rewards list
        self.create_rewards_list(paned)
        
        # Right side - Add reward form (for admins only)
        if self.controller.user_role == "admin":
            self.create_reward_form(paned)
        
        # Load initial data
        self.load_rewards()
    
    def create_header(self):
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        ttk.Label(
            header_frame, 
            text="Student Rewards",
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
            "Verified"
        )
        status_menu.pack(side=tk.LEFT, padx=5)
        
        # Apply filter button
        ttk.Button(
            filter_frame,
            text="Apply Filter",
            style='info.TButton',
            command=self.load_rewards
        ).pack(side=tk.LEFT, padx=5)
    
    def create_rewards_list(self, parent):
        list_frame = ttk.Frame(parent)
        parent.add(list_frame, weight=2)
        
        # Rewards list with scrollbar
        columns = ("id", "student_id", "student_name", "points", "item_name", "date_awarded", "status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=20)
        
        # Configure columns
        self.tree.heading("id", text="ID")
        self.tree.heading("student_id", text="Student ID")
        self.tree.heading("student_name", text="Student Name")
        self.tree.heading("points", text="Points")
        self.tree.heading("item_name", text="Item Returned")
        self.tree.heading("date_awarded", text="Date Awarded")
        self.tree.heading("status", text="Status")
        
        self.tree.column("id", width=50)
        self.tree.column("student_id", width=100)
        self.tree.column("student_name", width=150)
        self.tree.column("points", width=50)
        self.tree.column("item_name", width=150)
        self.tree.column("date_awarded", width=150)
        self.tree.column("status", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack items
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons
        button_frame = ttk.Frame(list_frame, padding=10)
        button_frame.pack(fill=tk.X)
        
        # Only admins can verify rewards
        if self.controller.user_role == "admin":
            ttk.Button(
                button_frame,
                text="Verify Reward",
                style='success.TButton',
                command=self.verify_selected_reward
            ).pack(side=tk.RIGHT, padx=5)
    
    def create_reward_form(self, parent):
        form_frame = ttk.Frame(parent, padding=10)
        parent.add(form_frame, weight=1)
        
        # Form title
        ttk.Label(
            form_frame, 
            text="Add Student Reward",
            font=('Helvetica', 16, 'bold')
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Form fields
        fields_frame = ttk.Frame(form_frame)
        fields_frame.pack(fill=tk.BOTH, expand=True)
        
        # Student ID
        ttk.Label(fields_frame, text="Student ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.student_id_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=self.student_id_var, width=30).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Student Name
        ttk.Label(fields_frame, text="Student Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.student_name_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=self.student_name_var, width=30).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Reward Points
        ttk.Label(fields_frame, text="Reward Points:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.points_var = tk.StringVar(value="10")
        ttk.Spinbox(
            fields_frame, 
            from_=1, 
            to=100, 
            textvariable=self.points_var, 
            width=5
        ).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Item Returned
        ttk.Label(fields_frame, text="Item Returned:").grid(row=3, column=0, sticky=tk.W, pady=5)
        
        # Get recovered items for dropdown
        recovered_items = get_recovered_items(self.controller.db_path)
        self.item_list = ["None"] + [f"{item['id']}: {item['item_name']}" for item in recovered_items]
        
        self.item_var = tk.StringVar(value=self.item_list[0])
        ttk.Combobox(
            fields_frame,
            textvariable=self.item_var,
            values=self.item_list,
            width=28,
            state="readonly"
        ).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            button_frame,
            text="Add Reward",
            style='success.TButton',
            command=self.add_reward
        ).pack(side=tk.RIGHT)
        
        ttk.Button(
            button_frame,
            text="Clear Form",
            style='secondary.TButton',
            command=self.clear_form
        ).pack(side=tk.RIGHT, padx=5)
    
    def load_rewards(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get filtered rewards
        status_filter = None if self.status_var.get() == "All" else self.status_var.get()
        rewards = get_rewards(self.controller.db_path, status_filter)
        
        # Add items to treeview
        for reward in rewards:
            self.tree.insert("", tk.END, values=(
                reward["id"],
                reward["student_id"],
                reward["student_name"],
                reward["reward_points"],
                reward["item_name"] or "N/A",
                reward["date_awarded"],
                reward["status"]
            ))
    
    def verify_selected_reward(self):
        # Get selected reward
        try:
            selected = self.tree.selection()[0]
            reward_id = self.tree.item(selected, "values")[0]
            current_status = self.tree.item(selected, "values")[6]
            
            if current_status == "Verified":
                messagebox.showinfo("Info", "This reward is already verified")
                return
            
            # Confirm action
            if messagebox.askyesno("Confirm", "Are you sure you want to verify this reward?"):
                # Verify the reward
                success = verify_reward(
                    self.controller.db_path,
                    reward_id,
                    self.controller.current_user
                )
                
                if success:
                    messagebox.showinfo("Success", "Reward verified successfully")
                    self.load_rewards()  # Refresh the list
        except IndexError:
            messagebox.showerror("Error", "Please select a reward")
    
    def add_reward(self):
        # Get form data
        student_id = self.student_id_var.get().strip()
        student_name = self.student_name_var.get().strip()
        points = self.points_var.get().strip()
        item = self.item_var.get()
        
        # Validate form
        if not student_id or not student_name:
            messagebox.showerror("Error", "Student ID and Name are required")
            return
        
        try:
            points = int(points)
            if points <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Points must be a positive number")
            return
        
        # Parse item ID if an item was selected
        item_id = None
        if item != "None":
            item_id = int(item.split(":")[0])
        
        # Add reward to database
        success = add_reward(
            self.controller.db_path,
            student_id,
            student_name,
            points,
            item_id
        )
        
        if success:
            messagebox.showinfo("Success", "Reward added successfully")
            self.clear_form()
            self.load_rewards()
    
    def clear_form(self):
        self.student_id_var.set("")
        self.student_name_var.set("")
        self.points_var.set("10")
        self.item_var.set(self.item_list[0])
