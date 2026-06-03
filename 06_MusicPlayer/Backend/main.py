# Libraries
import pathlib
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allows your React frontend to talk to your Python backend safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory where your MP3 files are stored
MUSIC_DIRECTORY = pathlib.Path(__file__).parent / "Songs"  # directory next to main.py
# Ensure the songs directory exists so listing won't crash
MUSIC_DIRECTORY.mkdir(parents=True, exist_ok=True)

@app.get("/songs")
def get_songs():
    """Scans your local folder and returns all MP3 filenames"""
    songs = [f.name for f in MUSIC_DIRECTORY.iterdir() if f.is_file() and f.suffix.lower() == ".mp3"]
    return {"songs": songs}

@app.get("/play/{song_name}")
def play_song(song_name: str):
    """Serves the raw MP3 file directly to your React audio player"""
    # Prevent path traversal by taking only the filename portion
    safe_name = pathlib.Path(song_name).name
    file_path = MUSIC_DIRECTORY / safe_name
    if file_path.exists() and file_path.is_file():
        print("File found:", file_path)
        return FileResponse(str(file_path), media_type="audio/mpeg")
    return {"error": "File not found"}