import customtkinter as ctk
from pathlib import Path
from PIL import Image, ImageTk

version = "v0.1.0"  # app version

# Directories
script_dir = Path(__file__).resolve().parent
assets_dir = script_dir / "assets"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"Dailyo {version}")  # Title
        self.geometry("400x300")  # Window size

        icon_path = assets_dir / "icon.ico"

        if icon_path.exists():
            # You don't need Pillow or ImageTk for this method!
            self.iconbitmap(str(icon_path))

if __name__ == "__main__":
    app = App()
    app.mainloop()