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

# Print startup info
print("=" * 60)
print("🎵 MUSIC PLAYER BACKEND STARTED")
print(f"📁 Main script location: {pathlib.Path(__file__).parent}")
print(f"📁 Songs directory: {MUSIC_DIRECTORY}")
print(f"📁 Songs directory exists: {MUSIC_DIRECTORY.exists()}")
if MUSIC_DIRECTORY.exists():
    try:
        files = list(MUSIC_DIRECTORY.iterdir())
        print(f"📁 Files in Songs folder: {[f.name for f in files]}")
    except Exception as e:
        print(f"❌ Error reading Songs folder: {e}")
print("=" * 60)

@app.get("/songs")
def get_songs():
    """Scans your local folder and returns all MP3 filenames"""
    print(f"📁 Scanning directory: {MUSIC_DIRECTORY}")
    print(f"📁 Directory exists: {MUSIC_DIRECTORY.exists()}")
    try:
        all_files = list(MUSIC_DIRECTORY.iterdir())
        print(f"📁 All files in directory: {[f.name for f in all_files]}")
        songs = [f.name for f in all_files if f.is_file() and f.suffix.lower() == ".mp3"]
        print(f"🎵 Found {len(songs)} MP3 songs: {songs}")
    except Exception as e:
        print(f"❌ Error scanning directory: {e}")
        songs = []
    return {"songs": songs}

@app.get("/debug")
def debug_info():
    """Debug endpoint to check if backend is working"""
    return {
        "status": "Backend is running!",
        "music_directory": str(MUSIC_DIRECTORY),
        "directory_exists": MUSIC_DIRECTORY.exists(),
        "files": [f.name for f in MUSIC_DIRECTORY.iterdir()] if MUSIC_DIRECTORY.exists() else []
    }

@app.get("/")
def root():
    """Root endpoint"""
    return {"status": "Music Player Backend is running"}

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

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Starting FastAPI server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)