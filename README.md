# Shazam‑like Audio Recognition Prototype

This repository contains a **minimal prototype** of the Shazam audio‑recognition system.

## 📖 Overview
- Record a short audio snippet (≈ 5 seconds) from a microphone.
- Convert the audio into a **spectrogram**, extract **spectral peaks**, and generate **hashes** (fingerprint).
- Look up the fingerprint in a **simple JSON database** of pre‑computed song fingerprints.
- Return the matching song's metadata (title, artist, album, year).

The implementation is deliberately lightweight and intended for **educational / demo** purposes – it is **not** a production‑grade Shazam clone.

## 📂 Project Structure
```
shazam_project/
├─ README.md                # This file
├─ requirements.txt         # Python dependencies
├─ fingerprint.py           # Core fingerprint generation
├─ database.json            # Simple fingerprint‑to‑metadata store
├─ database.example.json    # Example database structure
├─ app.py                   # Flask API exposing /identify and /ingest endpoints
├─ record_and_identify.py   # CLI tool to record audio and call the API
├─ ingest_youtube.py        # Script to download and ingest songs from YouTube
├─ test_with_file.py        # Test identification with an audio file
├─ reingest_all.py          # Reingest all downloaded songs
└─ utils.py                 # Helper utilities (audio loading, database operations)
```

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone <repository-url>
cd shazam_project
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

**Note:** You'll also need **FFmpeg** installed for audio processing:
- **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use `choco install ffmpeg`
- **macOS:** `brew install ffmpeg`
- **Linux:** `sudo apt-get install ffmpeg`

You'll also need **yt-dlp** for YouTube downloads:
```bash
pip install yt-dlp
```

### 3. Initialize the database
```bash
# Copy the example database structure
cp database.example.json database.json
```

### 4. Run the Flask server
```bash
python app.py
```
The server will listen on `http://127.0.0.1:5000`.

### 5. Ingest songs from YouTube
```bash
python ingest_youtube.py <youtube_url>
```
Example:
```bash
python ingest_youtube.py https://www.youtube.com/watch?v=jCVjudmnByk
```

### 6. Record and identify a song
```bash
python record_and_identify.py
```
Play a song for ~5 seconds; the script will send the audio to the server and print the result.

## 🎯 API Endpoints

### POST /identify
Identify a song from an audio file.

**Request:**
- `file`: Audio file (WAV, MP3, etc.)

**Response:**
```json
{
  "status": "success",
  "match": {
    "title": "Song Title",
    "artist": "Artist Name",
    "album": "Album Name",
    "score": 139
  }
}
```

### POST /ingest
Add a new song to the database.

**Request:**
- `file`: Audio file (WAV, MP3, etc.)
- `title`: Song title (optional)
- `artist`: Artist name (optional)
- `album`: Album name (optional)
- `year`: Release year (optional)

**Response:**
```json
{
  "status": "success",
  "message": "Added Song Title"
}
```

## 📚 How It Works

### Audio Fingerprinting
1. **Spectrogram Generation:** Convert audio to a time-frequency representation using STFT
2. **Peak Detection:** Identify local maxima in the spectrogram
3. **Hash Generation:** Create unique hashes from pairs of peaks (anchor + target)
4. **Database Lookup:** Match hashes against the fingerprint database
5. **Scoring:** Count matching hashes and return the best match

### Architecture
```
Client (Microphone) → Flask API → Fingerprint Generator → Database Lookup → Match Result
```

## 🔧 Scripts

- **`app.py`**: Flask server with `/identify` and `/ingest` endpoints
- **`record_and_identify.py`**: Record audio from microphone and identify
- **`ingest_youtube.py`**: Download and ingest songs from YouTube
- **`test_with_file.py`**: Test identification with a local audio file
- **`reingest_all.py`**: Reingest all songs in the downloads folder
- **`fingerprint.py`**: Core fingerprinting logic
- **`utils.py`**: Database and audio utilities

## 📘 System Design Reference

This prototype implements a simplified version of the Shazam audio recognition system:

### Functional Requirements
1. Capture ~5–10 seconds of audio through the client microphone
2. Generate fingerprints from spectrogram peaks and search against the catalog
3. Return matching song metadata (title, artist, album, year)

### Non-Functional Requirements
- **Accuracy:** Fingerprinting tolerates moderate noise/distortion
- **Speed:** Near real-time identification (< 5 seconds)
- **Scalability:** In production, would use distributed hash stores (Cassandra/HBase)

### Main Flow
1. Client records audio snippet and uploads to server
2. Backend converts to mono 22.05 kHz, computes spectrogram, extracts peaks
3. Creates hash triples `(f1, f2, Δt)` from anchor–target peak pairs
4. Queries hashes against fingerprint database
5. Returns top matching song or "no match"

### Production Considerations
For a production system, you would need:
- Distributed fingerprint storage (Cassandra, HBase, DynamoDB)
- CDN for audio/metadata delivery
- Caching layer (Redis)
- Load balancing and horizontal scaling
- Robust noise handling and preprocessing
- Monitoring and analytics

---

**License:** MIT

*This prototype is built for demonstration and educational purposes only. Real-world deployment would require a massive, distributed fingerprint database, robust noise handling, caching, and many other engineering concerns.*
