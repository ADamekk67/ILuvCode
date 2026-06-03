Project Overview

A lightweight Music Player web app built with:
- Frontend: React + Vite
- Backend: FastAPI
- Audio format: MP3

The app scans a local `Songs` folder, displays the MP3 playlist, and plays songs in the browser via HTML5 audio.

Key Features

Backend
- Lists MP3 files from the `Songs` folder
- Streams selected MP3 files
- Supports CORS for frontend/backend communication

Frontend
- Displays available tracks
- Highlights the selected song
- Uses browser audio controls
- Responsive two-panel layout

Project Structure

06_MusicPlayer
├── Backend
│   ├── main.py
│   ├── requirements.txt
│   └── Songs/
└── Frontend
    ├── src/
    │   ├── App.jsx
    │   ├── App.css
    │   └── main.jsx
    ├── package.json
    └── vite.config.js

Running the Application

Backend
```bash
cd 06_MusicPlayer/Backend
pip install -r requirements.txt
uvicorn main:app --reload
```
Backend runs on:
- `http://127.0.0.1:8000`

Frontend
```bash
cd 06_MusicPlayer/Frontend
npm install
npm run dev
```
Frontend runs on:
- `http://localhost:5173`

API Endpoints

Get song list
- `GET /songs`

Response example:
```json
{
  "songs": [
    "song1.mp3",
    "song2.mp3"
  ]
}
```

Play song
- `GET /play/{song_name}`

Example:
- `GET /play/song1.mp3`

Returns the MP3 audio stream directly.
