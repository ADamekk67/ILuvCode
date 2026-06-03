1. Introduction

The Music Player is a full-stack web application for browsing and playing locally stored MP3 files in the browser.

It consists of:
- A FastAPI backend for file discovery and audio delivery.
- A React frontend for user interaction and playback.

2. System Architecture

React frontend → FastAPI backend → Songs folder

Workflow:
1. User opens the React app.
2. React requests the available song list from FastAPI.
3. FastAPI scans the `Songs` directory.
4. FastAPI returns MP3 filenames as JSON.
5. User selects a track.
6. React requests the selected song stream.
7. FastAPI serves the MP3 file.
8. The browser audio player plays the song.

3. Backend Documentation

Technology:
- Python
- FastAPI
- Uvicorn

CORS configuration:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```
This allows the frontend to communicate with the API from a different port.

Songs directory:
```python
MUSIC_DIRECTORY = pathlib.Path(__file__).parent / "Songs"
MUSIC_DIRECTORY.mkdir(parents=True, exist_ok=True)
```
The backend creates this directory automatically if it does not exist.

Endpoints:

- `GET /songs`
  - Returns a JSON list of MP3 filenames.
  - Implementation:
    1. Scan the `Songs` folder.
    2. Filter files with `.mp3` extension.
    3. Return filenames in JSON.

Example response:
```json
{
  "songs": [
    "Imagine.mp3",
    "Believer.mp3",
    "Thunder.mp3"
  ]
}
```

- `GET /play/{song_name}`
  - Streams the requested MP3 file.
  - Protects against path traversal by using:
    ```python
    safe_name = pathlib.Path(song_name).name
    ```
  - Example safe path: `Songs/demo.mp3`

Success response:
```python
return FileResponse(
    str(file_path),
    media_type="audio/mpeg"
)
```

Error response:
```json
{
  "error": "File not found"
}
```

4. Frontend Documentation

Technology stack:
- React 19
- Vite
- CSS3

State management:
- `songs` stores the available track list.
- `currentSong` stores the currently selected track.

Backend connection:
```js
const BACKEND_URL = "http://127.0.0.1:8000";
```

Loading songs:
```js
useEffect(() => {
  fetch(`${BACKEND_URL}/songs`)
    .then((res) => res.json())
    .then((data) => setSongs(data.songs));
}, []);
```
Process:
- Call the `/songs` API.
- Receive JSON response.
- Update the song list.

Playlist rendering:
- Render each song as a clickable list item.
- Example list:
  - ▶ Imagine
  - ▶ Believer
  - ▶ Thunder

Song selection:
```js
onClick={() => setCurrentSong(song)}
```
Selected songs update the audio source.

Audio playback:
```jsx
<audio
  autoPlay
  controls
  src={`${BACKEND_URL}/play/${encodeURIComponent(currentSong)}`}
/>
```
Features:
- Play / pause
- Seek
- Volume control
- Auto-play after selection

5. User Interface Design

Layout:
- Two-column layout with a playlist on the left and now-playing details on the right.

Left panel:
- Playlist
- Track list

Right panel:
- Now Playing section
- Current track details
- Audio controls

Visual styling:
- Dark theme
- Green accent color
- Animated vinyl icon

Primary colors:
- Background: `#121212`
- Cards: `#181818`
- Accent: `#1db954`
- Hover: `#3e3e3e`

Vinyl animation:
```css
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
```
Duration: `4s linear infinite`

6. Installation Guide

Backend setup:
```bash
cd 06_MusicPlayer/Backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Frontend setup:
```bash
cd 06_MusicPlayer/Frontend
npm install
npm run dev
```

7. Requirements

Python packages:
- `fastapi`
- `uvicorn[standard]`

Node packages:
- `react`
- `react-dom`
- `vite`
- `eslint`

8. Future Improvements

Playback features:
- Next / previous buttons
- Shuffle mode
- Repeat mode
- Volume slider

Playlist features:
- Search
- Sort
- Multiple playlists
- Favorites

Metadata support:
- Album artwork
- Artist information
- Song duration
- Genre tags

Backend enhancements:
- Database integration
- User accounts
- Upload songs through UI
- Streaming optimization

9. Conclusion

This project demonstrates a full-stack Music Player built with FastAPI and React. It delivers a simple, extendable architecture for browsing and playing local MP3 files, with a user-friendly frontend and secure backend design.
