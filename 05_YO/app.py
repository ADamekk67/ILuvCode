import customtkinter as ctk
from pathlib import Path
import json

version = "v0.1.5"  # app version

# Directories
script_dir = Path(__file__).resolve().parent
assets_dir = script_dir / "assets"
settings_file = assets_dir / "settings.json"

# User Saved Data
assets_dir.mkdir(parents=True, exist_ok=True)

settings = {
        "WindowSize": (),
}
try:
    with settings_file.open('r') as f:
        loaded_data = json.load(f)
        settings.update(loaded_data)
except FileNotFoundError:
    print(f"{settings_file} not found - Starting with default settings.")



ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"

def save_settings():
    assets_dir.mkdir(parents=True, exist_ok=True)
    with settings_file.open('w') as f:
        json.dump(settings["WindowSize"], f, indent=4)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Save settings on close
        def on_closing():
            # Save window geometry before closing
            settings["window_geometry"] = self.geometry()
            save_settings()
            self.destroy()

        self.protocol("WM_DELETE_WINDOW", on_closing)

        self.title(f"YO {version}")  # Title
        
        # Load saved window size or use default
        if "window_geometry" in settings:
            self.geometry(settings["window_geometry"])
        else:
            self.geometry("800x600")  # Default window size

        icon_path = assets_dir / "icon.ico"

        if icon_path.exists():
            self.iconbitmap(str(icon_path))
        
        # Sidebar on the left for controls
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#2b2b2b")
        self.sidebar.pack(side="left", fill="y")

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(side="left", fill="both", expand=True)
        
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.add_note_button = ctk.CTkButton(self.sidebar, text="Add Note", command=self.add_note)
        self.add_note_button.pack(pady=10, padx=10)

    def add_note(self):
        note_text = ctk.CTkTextbox(self.content_frame, width=50, height=50)
        note_text.grid(row=0, column=0, padx=10, pady=10, sticky="n")

if __name__ == "__main__":
    app = App()
    app.mainloop()
