import tkinter as tk
import customtkinter as ctk
from pathlib import Path

version = "v0.1.7"  # app version

# Directories
script_dir = Path(__file__).resolve().parent
assets_dir = script_dir / "assets"
settings_file = assets_dir / "settings.json"

# Variables
window_size = "1200x600"
nodes = []

# Visual Variables
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"

class CustomizableFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        # Slightly wider and taller to fit our new interactive tools
        super().__init__(master, fg_color="#1F1F1F", border_width=2, corner_radius=6, width=250, height=220, **kwargs)
        
        # Prevent frame from collapsing around empty space
        self.pack_propagate(False)
        
        # 1. Editable Title (Replaces the static Label)
        # We use transparent background and low border width so it looks like a clean title until clicked
        self.title_entry = ctk.CTkEntry(
            self, 
            placeholder_text="Untitled", 
            font=("Arial", 13, "bold"), 
            fg_color="transparent", 
            border_width=1, 
            height=28
        )
        self.title_entry.pack(fill="x", padx=10, pady=(10, 5))
        
        # 2. Multi-line Content/Notes Area
        self.textbox = ctk.CTkTextbox(
            self, 
            fg_color="#1F1F1F", 
            corner_radius=4, 
            font=("Arial", 11)
        )
        self.textbox.pack(fill="both", expand=True, padx=10, pady=5)
        self.textbox.insert("0.0", "Text box...") # Default placeholder text

class ContextMenu(ctk.CTkFrame):
    def __init__(self, master, x, y, **kwargs):
        super().__init__(master, fg_color="#1F1F1F", border_width=1, corner_radius=6, **kwargs)
        
        # Store the click coordinates and master frame reference
        self.spawn_x = x
        self.spawn_y = y
        self.master_frame = master
        
        # Interactive buttons
        self.btn_option1 = ctk.CTkButton(self, text="New Frame", fg_color="transparent", hover_color="#67136E", height=25, command=self.action_new_custom_frame)
        self.btn_option1.pack(fill="x", padx=5, pady=3)
        
        self.btn_option2 = ctk.CTkButton(self, text="Clear All", fg_color="transparent", hover_color="#67136E", height=25, command=self.action_clear_all)
        self.btn_option2.pack(fill="x", padx=5, pady=3)

    def action_new_custom_frame(self): 
        # 1. Create the new frame inside the content_frame
        new_frame = CustomizableFrame(self.master_frame)
        # 2. Place it exactly where the context menu was opened
        new_frame.place(x=self.spawn_x, y=self.spawn_y)
        
        # 3. Track it in our nodes list
        nodes.append(new_frame)
        
        print(f"Spawned new frame at ({self.spawn_x}, {self.spawn_y})")
        self.destroy()

    def action_clear_all(self):
        # Cleanly destroy all existing nodes
        for node in nodes:
            if node.winfo_exists():
                node.destroy()
        nodes.clear()
        print("Cleared all custom frames.")
        self.destroy()

class App(ctk.CTk): 
    def __init__(self):
        super().__init__()

        # Save settings on close
        def on_closing():
            # save settings to file (placeholder)
            
            self.destroy()
            
        self.protocol("WM_DELETE_WINDOW", on_closing)

        self.title(f"YO {version}")  # Title
        self.geometry(window_size)  # Default size

        icon_path = assets_dir / "icon.ico"
        if icon_path.exists():
            self.iconbitmap(str(icon_path))
        else:
            print(f"Warning: Icon file not found at {icon_path}")
    
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Track the active menu instance so we can close it later
        self.active_menu = None
        
        # Bindings
        self.content_frame.bind("<Button-3>", self.right_click)  # Right-click event
        self.bind("<Button-1>", self.close_menu)  # Left-click anywhere to close menu

    def right_click(self, event): 
        # Clear any existing menu so they don't stack up infinitely
        if self.active_menu and self.active_menu.winfo_exists():
            self.active_menu.destroy()
            
        print(f"Right-click at: ({event.x}, {event.y})")
        
        # Spawn the new menu inside the content_frame, passing the click coordinates
        self.active_menu = ContextMenu(self.content_frame, x=event.x, y=event.y)
        self.active_menu.place(x=event.x, y=event.y)
        
    def close_menu(self, event):
        """Closes the menu if the user left-clicks outside of it."""
        if self.active_menu and self.active_menu.winfo_exists():
            clicked_widget = event.widget
            # Check if the clicked widget belongs to the context menu
            if not str(clicked_widget).startswith(str(self.active_menu)):
                self.active_menu.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()