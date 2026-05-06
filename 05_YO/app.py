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
    "Mode": "Light"
}
try:
    with settings_file.open('r') as f:
        loaded_data = json.load(f)
    settings["Mode"] = loaded_data.get("Mode", "Light")
except FileNotFoundError:
    print(f"{settings_file} not found - Starting with default settings.")
# 

current_mode = settings.get("Mode", "Light")
ctk.set_appearance_mode(current_mode)


def save_settings():
    assets_dir.mkdir(parents=True, exist_ok=True)
    with settings_file.open('w') as f:
        json.dump({"Mode": settings.get("Mode", "Light")}, f, indent=4)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Save settings on close
        def on_closing():
            save_settings()
            self.destroy()

        self.protocol("WM_DELETE_WINDOW", on_closing)

        self.title(f"YO {version}")  # Title
        self.geometry("800x600")  # Window size

        icon_path = assets_dir / "icon.ico"

        if icon_path.exists():
            self.iconbitmap(str(icon_path))
        
        # Sidebar on the left for controls
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#2b2b2b")
        self.sidebar.pack(side="left", fill="y")

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(side="left", fill="both", expand=True)

        def switch_theme():
            current_mode = ctk.get_appearance_mode()
            new_mode = "Dark" if current_mode == "Light" else "Light"
            ctk.set_appearance_mode(new_mode)
            settings["Mode"] = new_mode
            save_settings()

        theme_var = ctk.IntVar(value=1 if current_mode == "Dark" else 0)
        self.switch_theme_switch = ctk.CTkSwitch(
            self.sidebar,
            text="Dark Mode",
            command=switch_theme,
            variable=theme_var,
            onvalue=1,
            offvalue=0,
        )
        self.switch_theme_switch.pack(pady=(20, 10), padx=20, anchor="w")
                
        def show_config():
            config_window = ctk.CTkToplevel(self)
            config_window.title("Configuration")
            config_window.geometry("400x300")
            config_window.grab_set()  # Make the window modal

            label = ctk.CTkLabel(config_window, text="Configuration Settings", font=ctk.CTkFont(size=16, weight="bold"))
            label.pack(pady=20)

            # Add more configuration options here as needed
        show_config_button = ctk.CTkButton(self.sidebar, text="Configuration", command=show_config)
        show_config_button.pack(pady=10, padx=20, anchor="w")

if __name__ == "__main__":
    app = App()
    app.mainloop()
