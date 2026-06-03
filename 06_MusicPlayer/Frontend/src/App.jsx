import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [songs, setSongs] = useState([]);
  const [currentSong, setCurrentSong] = useState(null);

  // Backend URL (FastAPI default port is 8000)
  const BACKEND_URL = "http://127.0.0.1:8000";

  // 1. Fetch the song list from your Python backend when the app opens
  useEffect(() => {
    fetch(`${BACKEND_URL}/songs`)
      .then(response => response.json())
      .then(data => {
        if (data.songs) setSongs(data.songs);
      })
      .catch(err => console.error("Could not fetch songs from backend:", err));
  }, []);

  return (
    <div className="player-container">
      <header className="player-header">
        <h1> Hazzard - Song Player</h1>
      </header>

      <main className="player-body">
        {/* Left Side: Sidebar/Playlist view */}
        <section className="song-list-section">
          <h2>Your Tracks</h2>
          {songs.length === 0 ? (
            <p className="no-songs">No MP3s found. Drop some in your backend's "Songs" folder!</p>
          ) : (
            <ul className="song-list">
              {songs.map((song, index) => (
                <li 
                  key={index} 
                  className={`song-item ${currentSong === song ? 'active' : ''}`}
                  onClick={() => setCurrentSong(song)}
                >
                  <span className="note-icon">▶</span> {song.replace('.mp3', '')}
                </li>
              ))}
            </ul>
          )}
        </section>

        {/* Right Side: The Currently Playing Dashboard */}
        <section className="now-playing-section">
          <h2>Now Playing</h2>
          {currentSong ? (
            <div className="active-player">
              <div className="vinyl-disc">💿</div>
              <p className="current-title">{currentSong.replace('.mp3', '')}</p>
              
              {/* HTML5 Audio Player connecting directly to your Python API stream */}
              <audio 
                autoPlay 
                controls 
                src={`${BACKEND_URL}/play/${encodeURIComponent(currentSong)}`}
                className="audio-widget"
              />
            </div>
          ) : (
            <div className="empty-player">
              <p>Select a song from the list to start listening</p>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;