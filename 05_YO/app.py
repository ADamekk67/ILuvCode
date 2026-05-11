import customtkinter as ctk
from pathlib import Path
import json

version = "v0.1.6"  # app version

# Directories
script_dir = Path(__file__).resolve().parent
assets_dir = script_dir / "assets"
settings_file = assets_dir / "settings.json"
# constants
max_nodes = 20
# variables
window_size = ("1200x600")



ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"


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
    
        content_frame = ctk.CTkFrame(self)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        content_frame.bind("<Button-3>", self.on_right_click)  # Right-click event

    # on right-click event handler
    def on_right_click(self, event): # show menu on right-click
        print(f"Right-clicked at x={event.x}, y={event.y}")
        frame_menu = ctk.CTkFrame(self, width=150, height=100)


if __name__ == "__main__":
    app = App()
    app.mainloop()
