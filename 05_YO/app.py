import json
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
    def __init__(self, master, title="Untitled Node", text="Text box...", **kwargs):
        # Slightly wider and taller to fit our new interactive tools
        super().__init__(master, fg_color="#1F1F1F", border_width=2, corner_radius=6, width=250, height=220, **kwargs)
        
        # Prevent frame from collapsing around empty space
        self.pack_propagate(False)
        
        # Track the title string state
        self.title_text = title
        self.title_widget = None  # Holds either the Label or the Entry widget
        self._drag_data = {"x": 0, "y": 0, "orig_x": 0, "orig_y": 0}

        # Header area used for title editing and moving the frame
        self.header_frame = ctk.CTkFrame(self, fg_color="#1F1F1F", corner_radius=0, height=34)
        self.header_frame.pack(fill="x", padx=0, pady=(0, 5))
        self.header_frame.pack_propagate(False)

        self.move_handle = ctk.CTkLabel(self.header_frame, text="⇅", width=24, fg_color="transparent", anchor="center")
        self.move_handle.pack(side="right", padx=(0, 10))
        self.move_handle.bind("<Button-1>", self.start_move)
        self.move_handle.bind("<B1-Motion>", self.do_move)

        self.header_frame.bind("<Button-1>", self.start_move)
        self.header_frame.bind("<B1-Motion>", self.do_move)

        # 1. Main Textbox Content Area
        # We define this next so we can use it as a structural anchor for packing
        
        self.textbox = ctk.CTkTextbox(
            self, 
            fg_color="#1F1F1F", 
            corner_radius=4, 
            font=("Arial", 11)
        )
        self.textbox.pack(fill="both", expand=True, padx=10, pady=5)
        self.textbox.insert("0.0", text)

        # 2. Initialize the Title in Label Mode
        self.show_label_mode()
    
    def show_label_mode(self, event=None):
        """Swaps the title widget to a clean static Label."""
        # Clean up the previous widget if it exists
        if self.title_widget:
            self.title_widget.destroy()

        # Create the Label
        self.title_widget = ctk.CTkLabel(
            self.header_frame, 
            text=self.title_text, 
            font=("Arial", 13, "bold"),
            anchor="w" # Left-align the text
        )
        self.title_widget.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=5)
        
        # Bind the Double-Click event to enter Edit Mode
        self.title_widget.bind("<Double-Button-1>", self.show_edit_mode)

    def show_edit_mode(self, event=None):
        """Swaps the title widget to an editable Entry field."""
        if self.title_widget:
            self.title_widget.destroy()

        # Create the Entry field
        self.title_widget = ctk.CTkEntry(
            self.header_frame, 
            font=("Arial", 13, "bold"), 
            fg_color="transparent", 
            border_width=1, 
            height=28
        )
        self.title_widget.insert(0, self.title_text)
        self.title_widget.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=5)
        
        # Automatically focus the cursor into the field and select all text
        self.title_widget.focus()
        
        # Bindings to save and exit edit mode
        self.title_widget.bind("<Return>", self.save_title)    # Pressing Enter
        self.title_widget.bind("<FocusOut>", self.save_title)  # Clicking anywhere else

    def save_title(self, event=None):
        """Saves the input value and turns the entry back into a label."""
        if self.title_widget and isinstance(self.title_widget, ctk.CTkEntry):
            new_text = self.title_widget.get().strip()
            if new_text:  # Only update if the user actually typed something
                self.title_text = new_text
                
        # Revert back to the clean label
        self.show_label_mode()

    def get_state(self):
        """Returns the serializable state for this frame."""
        if self.title_widget and isinstance(self.title_widget, ctk.CTkEntry):
            self.save_title()

        return {
            "name": self.title_text,
            "text": self.textbox.get("0.0", "end-1c"),
            "x": self.winfo_x(),
            "y": self.winfo_y()
        }

    def start_move(self, event=None):
        """Begin moving the frame when the user clicks the header."""
        self._drag_data["x"] = event.x_root
        self._drag_data["y"] = event.y_root
        self._drag_data["orig_x"] = self.winfo_x()
        self._drag_data["orig_y"] = self.winfo_y()

    def do_move(self, event=None):
        """Move the frame while the user drags the header."""
        if not event:
            return

        dx = event.x_root - self._drag_data["x"]
        dy = event.y_root - self._drag_data["y"]
        new_x = self._drag_data["orig_x"] + dx
        new_y = self._drag_data["orig_y"] + dy

        if new_x < 0:
            new_x = 0
        if new_y < 0:
            new_y = 0

        self.place(x=new_x, y=new_y)

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

        self.switch_option3 = ctk.CTkSwitch(self, bg_color="#67136E")
        self.switch_option3.pack(fill="x", padx=5, pady=3)

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
            self.save_settings()
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

        self.load_settings()

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

    def save_settings(self):
        """Persist the current window and node state to the settings file."""
        node_data = [node.get_state() for node in nodes if node.winfo_exists()]
        payload = {
            "window_size": self.geometry(),
            "nodes": node_data
        }

        assets_dir.mkdir(parents=True, exist_ok=True)
        try:
            settings_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            print(f"Saved {len(node_data)} custom frame(s) to {settings_file}")
        except Exception as exc:
            print(f"Failed to save settings: {exc}")

    def load_settings(self):
        """Load saved frames and window geometry from the settings file."""
        if not settings_file.exists():
            return

        try:
            data = json.loads(settings_file.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"Failed to load settings: {exc}")
            return

        self.geometry(data.get("window_size", window_size))

        for node_state in data.get("nodes", []):
            frame = CustomizableFrame(
                self.content_frame,
                title=node_state.get("name", "Untitled Node"),
                text=node_state.get("text", "Text box...")
            )
            frame.place(x=node_state.get("x", 0), y=node_state.get("y", 0))
            nodes.append(frame)

if __name__ == "__main__":
    app = App()
    app.mainloop()