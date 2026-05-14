import tkinter as tk
import customtkinter as ctk
from pathlib import Path
import json

version = "v0.1.7"  # app version

# Directories
script_dir = Path(__file__).resolve().parent
assets_dir = script_dir / "assets"
settings_file = assets_dir / "settings.json"
# constants
max_nodes = 20

# variables
window_size = ("1200x600")
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
nodes = []

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
    
        content_frame = ctk.CTkFrame(self)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        content_frame.bind("<Button-3>", self.qm_on_right_click)  # Right-click event

        # create the right-click quick menu ( qm = quick menu )
        self.context_menu = tk.Menu(self, tearoff=0, font=("Arial", 12), bg="#333333", fg="#FFFFFF", activebackground="#555555", activeforeground="#FFFFFF")
        self.context_menu.add_command(label="New Node", command=lambda: self.qm_new_node()) # 1st menu item to create a new node
        self.context_menu.add_command(label="Settings", command=lambda: print("Open settings (placeholder)")) # 4th menu item to open settings (placeholder)

#
# Quick menu functions
#
    # on right-click event handler
    def qm_on_right_click(self, event):  # show menu on right-click
        print(f"Right-clicked at x={event.x}, y={event.y}")
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    # function to create a new node
    def qm_new_node(self):
        dialog = ctk.CTkInputDialog(title="New Node", text="Enter node name:")
        name = dialog.get_input()
        nodes.append(name)  # Add the new node to the list
        
        print(f"Created new node: {name}")

    for node in nodes:
        print(f"Node: {node}")
#
# Node menu functions
#




if __name__ == "__main__":
    app = App()
    app.mainloop()
